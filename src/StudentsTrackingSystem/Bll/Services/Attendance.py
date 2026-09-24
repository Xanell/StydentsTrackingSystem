from sqlalchemy.orm import Session
from Bll.Schemas.Attendance import AttendanceCreate, AttendanceDetail, AttendanceUpdate
from Dal.Repositories.Attendance import AttendanceRepository
from Dal.Repositories.Lessons import LessonsRepository
from Dal.Repositories.User import UserRepository
from Core.Enums import RoleName
from Core.Exceptions import NotFoundError, ConflictError, BusinessValidationError

class AttendanceService:
    def __init__(self, session: Session):
        self.attendance_repo = AttendanceRepository(session)
        self.lesson_repo = LessonsRepository(session)
        self.user_repo = UserRepository(session)

    def create_attendance(self, data: AttendanceCreate) -> AttendanceDetail:

        if self.lesson_repo.get_by_id(data.lesson_id) is None:
            raise NotFoundError(f"Урок #{data.lesson_id} не найден")

        student = self.user_repo.get_by_id(data.student_id)
        if student is None:
            raise NotFoundError(f"Пользователь #{data.student_id} не найден")
        if student.role.name != RoleName.USER:
            raise BusinessValidationError(f"Пользователь #{data.student_id} не является учеником")

        existing = self.attendance_repo.get_by_lesson_and_student(data.lesson_id, data.student_id)
        if existing is not None:
            raise ConflictError(f"Ученик #{data.student_id} уже отмечен на уроке #{data.lesson_id}")

        new_attendance = self.attendance_repo.create_attendance(
            lesson_id=data.lesson_id,
            student_id=data.student_id,
            is_present=data.is_present,
            reason=data.reason,
        )
        return AttendanceDetail.model_validate(new_attendance)

    def get_by_id(self, attendance_id: int) -> AttendanceDetail:
        attendance = self.attendance_repo.get_by_id(attendance_id)
        if attendance is None:
            raise NotFoundError("Ошибка: посещение не найдено!")
        return AttendanceDetail.model_validate(attendance)

    def get_all_attendances(self) -> list[AttendanceDetail]:
        all_attendances = self.attendance_repo.get_all()
        result = []
        for attendance in all_attendances:
            result.append(AttendanceDetail.model_validate(attendance))
        return result

    def get_by_lesson(self, lesson_id: int) -> list[AttendanceDetail]:
        attendances = self.attendance_repo.get_by_lesson(lesson_id)
        result = []
        for attendance in attendances:
            result.append(AttendanceDetail.model_validate(attendance))
        return result


    def update_attendance(self, attendance_id: int, data: AttendanceUpdate) -> AttendanceDetail:
        attendance = self.attendance_repo.get_by_id(attendance_id)
        if attendance is None:
            raise NotFoundError("Ошибка: посещение не найдено!")
        new_is_present = data.is_present if data.is_present is not None else attendance.is_present
        new_reason = data.reason if data.reason is not None else attendance.reason
        updated = self.attendance_repo.update_attendance(
            attendance_id,
            is_present=new_is_present,
            reason=new_reason,
        )
        return AttendanceDetail.model_validate(updated)