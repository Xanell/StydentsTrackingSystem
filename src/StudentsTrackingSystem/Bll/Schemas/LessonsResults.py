from Bll.Schemas.Base import BaseSchema
from Core.Enums import GradeType

class LessonResultDetail(BaseSchema):
    id: int
    lesson_id: int
    student_id: int
    file: str | None
    grade: int
    grade_type: GradeType

class LessonResultCreate(BaseSchema):
    lesson_id: int
    student_id: int
    file: str | None = None
    grade: int | None = None
    grade_type: GradeType

class LessonResultUpdate(BaseSchema):
    file: str | None = None
    grade: int | None = None
    grade_type: GradeType | None = None