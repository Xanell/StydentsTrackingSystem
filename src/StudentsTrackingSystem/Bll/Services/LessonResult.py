from sqlalchemy.orm import Session
from Bll.Schemas.LessonsResults import LessonResultCreate, LessonResultDetail, LessonResultUpdate
from Dal.Repositories.LessonsResults import LessonsResultsRepository
from Dal.Repositories.User import UserRepository
from Dal.Repositories.Lessons import LessonsRepository
from Core.Enums import RoleName
from datetime import datetime
from Core.Exceptions import NotFoundError, ConflictError, BusinessValidationError

class LessonsResultsService:
    def __init__(self, session: Session):
        self.result_repo = LessonsResultsRepository(session)
        self.lesson_repo = LessonsRepository(session)
        self.user_repo = UserRepository(session)

    def get_by_id(self, result_id: int) -> LessonResultDetail:
        result = self.result_repo.get_by_id(result_id)
        if result is None:
            raise NotFoundError("Ошибка: результат урока не найден!")
        return LessonResultDetail.model_validate(result)

    def get_all_results(self) -> list[LessonResultDetail]:
        all_results = self.result_repo.get_all()
        result = []
        for item in all_results:
            result.append(LessonResultDetail.model_validate(item))
        return result

    def get_by_lesson(self, lesson_id: int) -> list[LessonResultDetail]:
        results = self.result_repo.get_by_lesson(lesson_id)
        if result is None:
            raise NotFoundError("Ошибка: урок не найден")
        result = []
        for item in results:
            result.append(LessonResultDetail.model_validate(item))
        return result

    def get_by_student(self, student_id: int) -> list[LessonResultDetail]:
        results = self.result_repo.get_by_student(student_id)
        if result is None:
            raise NotFoundError("Ошибка: студент не найден!")
        result = []
        for item in results:
            result.append(LessonResultDetail.model_validate(item))
        return result

    def create_result(self, data: LessonResultCreate) -> LessonResultDetail:

        if self.lesson_repo.get_by_id(data.lesson_id) is None:
            raise NotFoundError(f"Урок #{data.lesson_id} не найден")
        
        student = self.user_repo.get_by_id(data.student_id)
        if student is None:
            raise NotFoundError(f"Пользователь #{data.student_id} не найден")
        if student.role.name != RoleName.USER:
            raise BusinessValidationError(f"Пользователь #{data.student_id} не является учеником")

        existing = self.result_repo.get_by_lesson_and_student(data.lesson_id, data.student_id)
        if existing is not None:
            raise ConflictError(
                f"У ученика #{data.student_id} уже есть результат за урок #{data.lesson_id}"
            )
        
        if data.grade is None:
            raise BusinessValidationError("Ошибка: оценка обязательна!")

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
            raise NotFoundError("Ошибка: результат урока не найден!")
        
        new_file = data.file if data.file is not None else result.file
        new_grade = data.grade if data.grade is not None else result.grade
        new_grade_type = data.grade_type if data.grade_type is not None else result.grade_type
        
        updated = self.result_repo.update_lesson_result(
            result_id,
            file=new_file,
            grade=new_grade,
            grade_type=new_grade_type,
        )
        return LessonResultDetail.model_validate(updated)