import { apiFetch } from "../lib/apiClient";
import type { Course, Day, Meeting, NewCourse } from "../types/schedule";

type BackendMeeting = {
  day: Day;
  start_time: string;
  end_time: string;
};

type BackendCourse = {
  id: number;
  name: string;
  doctor: string | null;
  section: string | null;
  building: string | null;
  room: string | null;
  meetings: BackendMeeting[];
};

export async function getCourses(): Promise<Course[]> {
  const response = await apiFetch("/api/courses");

  if (!response.ok) {
    throw new Error("Failed to load courses");
  }

  const data: BackendCourse[] = await response.json();

  return data.map((course) => ({
    id: course.id,
    name: course.name,

    doctor: course.doctor ?? undefined,
    section: course.section ?? undefined,
    building: course.building ?? undefined,
    room: course.room ?? undefined,

    meetings: course.meetings.map((meeting) => ({
      day: meeting.day,

      startTime: meeting.start_time.slice(0, 5),
      endTime: meeting.end_time.slice(0, 5),
    })),
  }));
}

export async function createCourse(newCourse: NewCourse): Promise<Course> {
  const response = await apiFetch("/api/courses", {
    method: "POST",
    body: JSON.stringify(newCourse),
  });

  if (!response.ok) {
    throw new Error("Failed to create course");
  }

  const course: BackendCourse = await response.json();

  return {
    id: course.id,
    name: course.name,

    doctor: course.doctor ?? undefined,
    section: course.section ?? undefined,
    building: course.building ?? undefined,
    room: course.room ?? undefined,

    meetings: course.meetings.map((meeting) => ({
      day: meeting.day,
      startTime: meeting.start_time.slice(0, 5),
      endTime: meeting.end_time.slice(0, 5),
    })),
  };
}

export async function updateCourse(
  courseId: number,
  updatedCourse: NewCourse,
): Promise<Course> {
  const response = await apiFetch(`/api/courses/${courseId}`, {
    method: "PUT",
    body: JSON.stringify(updatedCourse),
  });

  if (!response.ok) {
    throw new Error("Failed to update course");
  }

  const course: BackendCourse = await response.json();

  return {
    id: course.id,
    name: course.name,
    doctor: course.doctor ?? undefined,
    section: course.section ?? undefined,
    building: course.building ?? undefined,
    room: course.room ?? undefined,

    meetings: course.meetings.map((meeting) => ({
      day: meeting.day,
      startTime: meeting.start_time.slice(0, 5),
      endTime: meeting.end_time.slice(0, 5),
    })),
  };
}

export async function updateCourseMeeting(
  courseId: number,
  originalMeeting: Meeting,
  updatedMeeting: Meeting,
): Promise<Meeting> {
  const response = await apiFetch(`/api/courses/${courseId}/meeting`, {
    method: "PATCH",
    body: JSON.stringify({
      originalMeeting,
      updatedMeeting,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to update meeting");
  }

  const meeting: BackendMeeting = await response.json();

  return {
    day: meeting.day,
    startTime: meeting.start_time.slice(0, 5),
    endTime: meeting.end_time.slice(0, 5),
  };
}
export async function deleteCourse(courseId: number): Promise<void> {
  const response = await apiFetch(`/api/courses/${courseId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete course");
  }
}

export async function deleteCourseMeeting(
  courseId: number,
  meeting: Meeting,
): Promise<void> {
  const params = new URLSearchParams({
    day: meeting.day,
    start_time: meeting.startTime,
    end_time: meeting.endTime,
  });

  const response = await apiFetch(
    `/api/courses/${courseId}/meeting?${params.toString()}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    throw new Error("Failed to delete meeting");
  }
}
