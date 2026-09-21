from sqlalchemy.orm import Session
from Bll.Schemas.LessonsResults import LessonResultCreate, LessonResultDetail, LessonResultUpdate
from Dal.Repositories.LessonsResults import LessonsResultsRepository
from datetime import datetime

class LessonsResultsService:
    def __init__(self, session: Session):
        self.result_repo = LessonsResultsRepository(session)

    def get_by_id(self, result_id: int) -> LessonResultDetail:
        result = self.result_repo.get_by_id(result_id)
        if result is None:
            raise ValueError("Ошибка: результат урока не найден!")
        return LessonResultDetail.model_validate(result)

    def get_all_results(self) -> list[LessonResultDetail]:
        all_results = self.result_repo.get_all()
        result = []
        for item in all_results:
            result.append(LessonResultDetail.model_validate(item))
        return result

    def get_by_lesson(self, lesson_id: int) -> list[LessonResultDetail]:
        results = self.result_repo.get_by_lesson(lesson_id)
        result = []
        for item in results:
            result.append(LessonResultDetail.model_validate(item))
        return result

    def get_by_student(self, student_id: int) -> list[LessonResultDetail]:
        results = self.result_repo.get_by_student(student_id)
        result = []
        for item in results:
            result.append(LessonResultDetail.model_validate(item))
        return result

    def create_result(self, data: LessonResultCreate) -> LessonResultDetail:
        if data.grade is None:
            raise ValueError("Ошибка: оценка обязательна!")

        new_result = self.result_repo.create_result(
            lesson_id=data.lesson_id,
            student_id=data.student_id,
            file=data.file,
            grade=data.grade,
            grade_type=data.grade_type,
            submitted_at=datetime.now(),
        )
        return LessonResultDetail.model_validate(new_result)

    def update_result(self, result_id: int, data: LessonResultUpdate) -> LessonResultDetail:
        result = self.result_repo.get_by_id(result_id)
        if result is None:
            raise ValueError("Ошибка: результат урока не найден!")
        updated = self.result_repo.update_lesson_result(
            result_id,
            grade=data.grade,
            grade_type=data.grade_type,
            submitted_at=datetime.now(),
        )
        return LessonResultDetail.model_validate(updated)