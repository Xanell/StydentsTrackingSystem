from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.LessonsResults import LessonsResults
from datetime import datetime


class LessonsResultsRepository:
    # Конструктор: принимает сессию БД
    def __init__(self, session: Session):
        self.session = session

    # Создаёт новую оценку и сохраняет в БД
    def add_result(self, lesson_id: int, student_id: int, grade: int, grade_type: str, submitted_at: datetime) -> LessonsResults:
        result = LessonsResults(
            lesson_id=lesson_id,
            student_id=student_id,
            grade=grade,
            grade_type=grade_type,
            submitted_at=submitted_at
        )
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result

    # Ищет оценку по id
    def get_by_id(self, result_id: int) -> LessonsResults | None:
        stmt = select(LessonsResults).where(LessonsResults.id == result_id)
        return self.session.scalar(stmt).one_or_none()

    # Возвращает все оценки
    def get_all(self) -> list[LessonsResults]:
        stmt = select(LessonsResults).order_by(LessonsResults.submitted_at.desc())
        return list(self.session.scalars(stmt).all())

    # Возвращает все оценки по конкретному уроку
    def get_by_lesson(self, lesson_id: int) -> list[LessonsResults]:
        stmt = select(LessonsResults).where(LessonsResults.lesson_id == lesson_id)
        return list(self.session.scalars(stmt).all())

    # Возвращает все оценки конкретного студента
    def get_by_student(self, student_id: int) -> list[LessonsResults]:
        stmt = select(LessonsResults).where(LessonsResults.student_id == student_id)
        return list(self.session.scalars(stmt).all())

    # Возвращает оценку конкретного студента за конкретный урок
    def get_by_lesson_and_student(self, lesson_id: int, student_id: int) -> LessonsResults | None:
        stmt = select(LessonsResults).where(
            LessonsResults.lesson_id == lesson_id,
            LessonsResults.student_id == student_id
        )
        return self.session.scalar(stmt).one_or_none()

    # Обновляет оценку
    def update(self, result_id: int, grade: int | None = None, grade_type: str | None = None, submitted_at: datetime | None = None) -> LessonsResults | None:
        result = self.get_by_id(result_id)
        if result is None:
            return None
        if grade is not None:
            result.grade = grade
        if grade_type is not None:
            result.grade_type = grade_type
        if submitted_at is not None:
            result.submitted_at = submitted_at
        self.session.commit()
        self.session.refresh(result)
        return result

    # Удаляет оценку по id
    def delete(self, result_id: int) -> bool:
        result = self.get_by_id(result_id)
        if result is None:
            return False
        self.session.delete(result)
        self.session.commit()
        return True