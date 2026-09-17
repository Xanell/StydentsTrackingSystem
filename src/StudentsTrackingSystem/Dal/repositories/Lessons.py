from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Lessons import Lessons
from datetime import date


class LessonsRepository:
    # Конструктор: принимает сессию БД
    def __init__(self, session: Session):
        self.session = session

    # Создаёт новый урок и сохраняет в БД
    def add_lesson(self, date: date, topic: str, homework_description: str, homework_due_date: date, files: str, schedule_id: int) -> Lessons:
        lesson = Lessons(
            date=date,
            topic=topic,
            homework_description=homework_description,
            homework_due_date=homework_due_date,
            files=files,
            schedule_id=schedule_id
        )
        self.session.add(lesson)
        self.session.commit()
        self.session.refresh(lesson)
        return lesson

    # Ищет урок по id
    def get_by_id(self, lesson_id: int) -> Lessons | None:
        stmt = select(Lessons).where(Lessons.id == lesson_id)
        return self.session.scalar(stmt).one_or_none()

    # Возвращает все уроки, отсортированные по дате (сначала новые)
    def get_all(self) -> list[Lessons]:
        stmt = select(Lessons).order_by(Lessons.date.desc())
        return list(self.session.scalars(stmt).all())

    # Возвращает все уроки на конкретную дату
    def get_by_date(self, date: date) -> list[Lessons]:
        stmt = select(Lessons).where(Lessons.date == date)
        return list(self.session.scalars(stmt).all())

    # Возвращает все уроки по конкретному расписанию (schedule_id)
    def get_by_schedule(self, schedule_id: int) -> list[Lessons]:
        stmt = select(Lessons).where(Lessons.schedule_id == schedule_id)
        return list(self.session.scalars(stmt).all())

    # Обновляет данные урока
    def update(self, lesson_id: int, date: date | None = None, topic: str | None = None, homework_description: str | None = None, homework_due_date: date | None = None, files: str | None = None) -> Lessons | None:
        lesson = self.get_by_id(lesson_id)
        if lesson is None:
            return None
        if date is not None:
            lesson.date = date
        if topic is not None:
            lesson.topic = topic
        if homework_description is not None:
            lesson.homework_description = homework_description
        if homework_due_date is not None:
            lesson.homework_due_date = homework_due_date
        if files is not None:
            lesson.files = files
        self.session.commit()
        self.session.refresh(lesson)
        return lesson

    # Удаляет урок по id
    def delete(self, lesson_id: int) -> bool:
        lesson = self.get_by_id(lesson_id)
        if lesson is None:
            return False
        self.session.delete(lesson)
        self.session.commit()
        return True