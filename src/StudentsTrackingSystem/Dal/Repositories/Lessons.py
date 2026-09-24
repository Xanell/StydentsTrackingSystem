from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Lessons import Lesson
from datetime import date

class LessonsRepository:
    # Конструктор: принимает сессию БД
    def __init__(self, session: Session):
        self.db = session

    # Создаёт новый урок и сохраняет в БД
    def create_lesson(self, lesson_date: date, topic: str, homework_description: str | None, homework_due_date: date | None, files: str | None, schedule_id: int) -> Lesson:
        lesson = Lesson(
            lesson_date=lesson_date,
            topic=topic,
            homework_description=homework_description,
            homework_due_date=homework_due_date,
            files=files,
            schedule_id=schedule_id
        )
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)
        return lesson

    # Ищет урок по id
    def get_by_id(self, lesson_id: int) -> Lesson | None:
        return self.db.get(Lesson, lesson_id)

    # Возвращает все уроки, отсортированные по дате (сначала новые)
    def get_all(self) -> list[Lesson]:
        stmt = select(Lesson).order_by(Lesson.lesson_date.desc())
        return self.db.scalars(stmt).all()

    # Возвращает все уроки на конкретную дату
    def get_by_date(self, lesson_date: date) -> list[Lesson]:
        stmt = select(Lesson).where(Lesson.lesson_date == lesson_date)
        return self.db.scalars(stmt).all()

    # Возвращает все уроки по конкретному расписанию (schedule_id)
    def get_by_schedule(self, schedule_id: int) -> list[Lesson]:
        stmt = select(Lesson).where(Lesson.schedule_id == schedule_id)
        return self.db.scalars(stmt).all()

    # Возможно стоит добавить в будущем lesson_date: date | None = None
    def update_lesson(self, lesson_id: int, topic: str | None = None, homework_description: str | None = None, homework_due_date: date | None = None, files: str | None = None) -> Lesson | None:
        lesson = self.get_by_id(lesson_id)
        if lesson is None:
            return None
        if topic is not None:
            lesson.topic = topic
        if homework_description is not None:
            lesson.homework_description = homework_description
        if homework_due_date is not None:
            lesson.homework_due_date = homework_due_date
        if files is not None:
            lesson.files = files
        self.db.commit()
        self.db.refresh(lesson)
        return lesson
