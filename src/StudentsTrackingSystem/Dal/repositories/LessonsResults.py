from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.LessonsResults import LessonResult
from ...Core.Enums import GradeType
from datetime import datetime

class LessonsResultsRepository:
    # Конструктор: принимает сессию БД
    def __init__(self, session: Session):
        self.db = session

    # Создаёт новую оценку и сохраняет в БД
    def create_result(self, lesson_id: int, student_id: int, file: str | None, grade: int, grade_type: GradeType, submitted_at: datetime) -> LessonResult:
        result = LessonResult(
            lesson_id=lesson_id,
            student_id=student_id,
            file=file,
            grade=grade,
            grade_type=grade_type,
            submitted_at=submitted_at
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    # Ищет оценку по id
    def get_by_id(self, result_id: int) -> LessonResult | None:
        return self.db.get(LessonResult, result_id)

    # Возвращает все оценки
    def get_all(self) -> list[LessonResult]:
        stmt = select(LessonResult).order_by(LessonResult.submitted_at.desc())
        return self.db.scalars(stmt).all()

    # Возвращает все оценки по конкретному уроку
    def get_by_lesson(self, lesson_id: int) -> list[LessonResult]:
        stmt = select(LessonResult).where(LessonResult.lesson_id == lesson_id)
        return self.db.scalars(stmt).all()

    # Возвращает все оценки конкретного студента
    def get_by_student(self, student_id: int) -> list[LessonResult]:
        stmt = select(LessonResult).where(LessonResult.student_id == student_id)
        return self.db.scalars(stmt).all()

    # Возвращает оценку конкретного студента за конкретный урок
    def get_by_lesson_and_student(self, lesson_id: int, student_id: int) -> LessonResult | None:
        stmt = select(LessonResult).where(
            LessonResult.lesson_id == lesson_id,
            LessonResult.student_id == student_id
        )
        return self.db.scalars(stmt).one_or_none()

    # Обновляет оценку
    def update_lesson_result(self, result_id: int, grade: int | None = None, grade_type: GradeType | None = None, submitted_at: datetime | None = None) -> LessonResult | None:
        result = self.get_by_id(result_id)
        if result is None:
            return None
        if grade is not None:
            result.grade = grade
        if grade_type is not None:
            result.grade_type = grade_type
        if submitted_at is not None:
            result.submitted_at = submitted_at
        self.db.commit()
        self.db.refresh(result)
        return result

    # Удаляет оценку по id
    def delete_result(self, result_id: int) -> bool:
        result = self.get_by_id(result_id)
        if result is None:
            return False
        self.db.delete(result)
        self.db.commit()
        return True