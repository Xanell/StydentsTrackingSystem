from datetime import datetime
from pydantic import Field
from Bll.Schemas.Base import BaseSchema
from Bll.Schemas.User import UserShort

class HomeworkSubmissionDetail(BaseSchema):
    """file_path не входит — как и у материалов урока, файл отдаёт сервис."""

    id: int
    lesson_id: int
    student: UserShort
    original_name: str
    comment: str | None
    submitted_at: datetime

class HomeworkSubmissionCreate(BaseSchema):
    """
    Текстовая часть сдачи. Файл приходит из request.FILES,
    а student_id сервис берёт из текущего пользователя, а не из формы.
    """

    lesson_id: int
    comment: str | None = Field(default=None, max_length=500)
