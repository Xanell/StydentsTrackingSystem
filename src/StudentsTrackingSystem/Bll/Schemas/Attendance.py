from pydantic import Field
from Bll.Schemas.Base import BaseSchema

class AttendanceDetail(BaseSchema):
    id: int
    lesson_id: int
    student_id: int
    is_present: bool
    reason: str | None

class AttendanceItem(BaseSchema):
    """Отметка одного ученика в форме посещаемости."""

    student_id: int
    is_present: bool = True
    reason: str | None = Field(default=None, max_length=255)  # у присутствующих сбрасывается в None

class AttendanceSave(BaseSchema):
    """Вся форма посещаемости за урок (AttendanceRepository.save_for_lesson)."""

    lesson_id: int
    items: list[AttendanceItem]

class AttendanceUpdate(BaseSchema):
    """Исправить одну отметку: например, ошибочную «Н»."""

    is_present: bool
    reason: str | None = Field(default=None, max_length=255)
