from pydantic import BaseModel


class MeetingInput(BaseModel):
    day: str
    startTime: str
    endTime: str


class MeetingUpdateInput(BaseModel):
    originalMeeting: MeetingInput
    updatedMeeting: MeetingInput


class CourseInput(BaseModel):
    name: str
    doctor: str | None = None
    section: str | None = None
    building: str | None = None
    room: str | None = None
    meetings: list[MeetingInput]