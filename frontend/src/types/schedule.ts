export type Day =
  | "sunday"
  | "monday"
  | "tuesday"
  | "wednesday"
  | "thursday"
  | "friday"
  | "saturday";

export type Meeting = {
  day: Day;
  startTime: string;
  endTime: string;
};

export type Course = {
  id: number;
  name: string;
  doctor?: string;
  building?: string;
  room?: string;
  section?: string;
  meetings: Meeting[];
};

export type NewCourse = Omit<Course, "id">;
