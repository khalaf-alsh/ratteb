import httpx

from fastapi import APIRouter, Depends, HTTPException

from app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY
from app.dependencies.auth import get_authenticated_user
from app.models.schedule import (
    CourseInput,
    MeetingUpdateInput,
)


router = APIRouter(
    prefix="/api/courses",
    tags=["Courses"],
)


@router.get("")
async def get_courses(
    auth=Depends(get_authenticated_user),
):
    access_token, _ = auth

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "select": (
            "id,"
            "name,"
            "doctor,"
            "section,"
            "building,"
            "room,"
            "meetings(day,start_time,end_time)"
        )
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/courses",
            headers=headers,
            params=params,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to load courses",
        )

    return response.json()


@router.post("", status_code=201)
async def create_course(
    course: CourseInput,
    auth=Depends(get_authenticated_user),
):
    access_token, user = auth

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    course_data = {
        "user_id": user.id,
        "name": course.name,
        "doctor": course.doctor,
        "section": course.section,
        "building": course.building,
        "room": course.room,
    }

    async with httpx.AsyncClient() as client:
        course_response = await client.post(
            f"{SUPABASE_URL}/rest/v1/courses",
            headers=headers,
            json=course_data,
        )

        if course_response.status_code >= 400:
            raise HTTPException(
                status_code=course_response.status_code,
                detail="Failed to create course",
            )

        created_course = course_response.json()[0]
        course_id = created_course["id"]

        meetings_data = [
            {
                "course_id": course_id,
                "day": meeting.day,
                "start_time": meeting.startTime,
                "end_time": meeting.endTime,
            }
            for meeting in course.meetings
        ]

        meetings_response = await client.post(
            f"{SUPABASE_URL}/rest/v1/meetings",
            headers=headers,
            json=meetings_data,
        )

        if meetings_response.status_code >= 400:
            await client.delete(
                f"{SUPABASE_URL}/rest/v1/courses?id=eq.{course_id}",
                headers=headers,
            )

            raise HTTPException(
                status_code=meetings_response.status_code,
                detail="Failed to create course meetings",
            )

    return {
        "id": course_id,
        "name": course.name,
        "doctor": course.doctor,
        "section": course.section,
        "building": course.building,
        "room": course.room,
        "meetings": [
            {
                "day": meeting.day,
                "start_time": meeting.startTime,
                "end_time": meeting.endTime,
            }
            for meeting in course.meetings
        ],
    }


@router.put("/{course_id}")
async def update_course(
    course_id: int,
    course: CourseInput,
    auth=Depends(get_authenticated_user),
):
    access_token, _ = auth

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    course_data = {
        "name": course.name,
        "doctor": course.doctor,
        "section": course.section,
        "building": course.building,
        "room": course.room,
    }

    async with httpx.AsyncClient() as client:
        course_response = await client.patch(
            f"{SUPABASE_URL}/rest/v1/courses?id=eq.{course_id}",
            headers=headers,
            json=course_data,
        )

        if course_response.status_code >= 400:
            raise HTTPException(
                status_code=course_response.status_code,
                detail="Failed to update course",
            )

        delete_response = await client.delete(
            f"{SUPABASE_URL}/rest/v1/meetings?course_id=eq.{course_id}",
            headers=headers,
        )

        if delete_response.status_code >= 400:
            raise HTTPException(
                status_code=delete_response.status_code,
                detail="Failed to update course meetings",
            )

        meetings_data = [
            {
                "course_id": course_id,
                "day": meeting.day,
                "start_time": meeting.startTime,
                "end_time": meeting.endTime,
            }
            for meeting in course.meetings
        ]

        meetings_response = await client.post(
            f"{SUPABASE_URL}/rest/v1/meetings",
            headers=headers,
            json=meetings_data,
        )

        if meetings_response.status_code >= 400:
            raise HTTPException(
                status_code=meetings_response.status_code,
                detail="Failed to save updated meetings",
            )

    return {
        "id": course_id,
        "name": course.name,
        "doctor": course.doctor,
        "section": course.section,
        "building": course.building,
        "room": course.room,
        "meetings": [
            {
                "day": meeting.day,
                "start_time": meeting.startTime,
                "end_time": meeting.endTime,
            }
            for meeting in course.meetings
        ],
    }


@router.patch("/{course_id}/meeting")
async def update_course_meeting(
    course_id: int,
    meeting_update: MeetingUpdateInput,
    auth=Depends(get_authenticated_user),
):
    access_token, _ = auth

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    original = meeting_update.originalMeeting
    updated = meeting_update.updatedMeeting

    meeting_data = {
        "day": updated.day,
        "start_time": updated.startTime,
        "end_time": updated.endTime,
    }

    url = (
        f"{SUPABASE_URL}/rest/v1/meetings"
        f"?course_id=eq.{course_id}"
        f"&day=eq.{original.day}"
        f"&start_time=eq.{original.startTime}"
        f"&end_time=eq.{original.endTime}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url,
            headers=headers,
            json=meeting_data,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to update meeting",
        )

    updated_rows = response.json()

    if not updated_rows:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found",
        )

    updated_row = updated_rows[0]

    return {
        "day": updated_row["day"],
        "start_time": updated_row["start_time"],
        "end_time": updated_row["end_time"],
    }


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: int,
    auth=Depends(get_authenticated_user),
):
    access_token, _ = auth

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{SUPABASE_URL}/rest/v1/courses?id=eq.{course_id}",
            headers=headers,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to delete course",
        )


@router.delete("/{course_id}/meeting", status_code=204)
async def delete_course_meeting(
    course_id: int,
    day: str,
    start_time: str,
    end_time: str,
    auth=Depends(get_authenticated_user),
):
    access_token, _ = auth

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    url = (
        f"{SUPABASE_URL}/rest/v1/meetings"
        f"?course_id=eq.{course_id}"
        f"&day=eq.{day}"
        f"&start_time=eq.{start_time}"
        f"&end_time=eq.{end_time}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            url,
            headers=headers,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to delete meeting",
        )