from sqlalchemy.orm import Session
from Bll.Schemas.Lessons import LessonDetail, LessonCreate, LessonUpdate
from Dal.Repositories.Lessons import LessonsRepository
from datetime import date

class LessonService:
    def __init__(self, session: Session):
        self.lesson_repo = LessonsRepository(session)

    def get_by_id(self, lesson_id) -> LessonDetail:
        Lesson = self.lesson_repo.get_by_id(lesson_id)
        if Lesson is None:
            raise ValueError("Ошибка урок не найден")
        return LessonDetail.model_validate(Lesson)

    def get_all_lessons(self) -> list[LessonDetail]:
        all_lessons = self.lesson_repo.get_all()
        result = []
        for lesson in all_lessons:
            result.append(LessonDetail.model_validate(lesson))
        return result

    def get_by_schedule(self, schedule_id: int) -> list[LessonDetail]:
        lessons = self.lesson_repo.get_by_schedule(schedule_id)
        result = []
        for lesson in lessons:
            result.append(LessonDetail.model_validate(lesson))
        return result

    def get_by_date(self, lesson_date: date) -> list[LessonDetail]:
        lessons = self.lesson_repo.get_by_date(lesson_date)
        result = []
        for lesson in lessons:
            result.append(LessonDetail.model_validate(lesson))
        return result