from Bll.Schemas.Base import BaseSchema
from datetime import date

class LessonDetail(BaseSchema):
    id: int
    lesson_date: date
    topic: str
    homework_description: str | None
    homework_due_date: date | None
    files: str | None

class LessonCreate(BaseSchema):
    lesson_date: date
    topic: str
    homework_description: str | None = None
    homework_due_date: date | None = None
    files: str | None = None
    schedule_id: int

class LessonUpdate(BaseSchema):
    topic: str | None = None
    homework_description: str | None = None
    homework_due_date: date | None = None
    files: str | None = None