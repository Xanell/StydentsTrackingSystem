from datetime import datetime
from Bll.Schemas.Base import BaseSchema

class LessonFileDetail(BaseSchema):
    """
    Материал урока для показа на странице. file_path сюда намеренно не входит:
    путь на диске нужен только сервису, который отдаёт файл после проверки прав.
    Схемы Create нет: файл приходит из request.FILES и передаётся в сервис напрямую.
    """

    id: int
    lesson_id: int
    original_name: str
    uploaded_at: datetime
