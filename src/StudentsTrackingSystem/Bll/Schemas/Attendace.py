from Bll.Schemas.Base import BaseSchema

class AttendanceDetail(BaseSchema):
    id: int
    lesson_id: int
    student_id: int
    is_present: bool
    reason: str | None

class AttendanceCreate(BaseSchema):
    lesson_id: int
    student_id: int
    is_present: bool
    reason: str | None = None

class AttendanceUpdate(BaseSchema):
    is_present: bool | None = None
    reason: str | None = None