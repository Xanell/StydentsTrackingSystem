from sqlalchemy.orm import Session
from Bll.Schemas.Attendance import (
    AttendanceCreate,
    AttendanceDetail,
    AttendanceUpdate,
)
from Dal.Repositories.Attendance import AttendanceRepository

class AttendanceService:
    def __init__(self, session: Session):
        self.attendance_repo = AttendanceRepository(session)

    def get_by_id(self, attendance_id: int) -> AttendanceDetail:
        attendance = self.attendance_repo.get_by_id(attendance_id)
        if attendance is None:
            raise ValueError("Ошибка: посещение не найдено!")
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

    def create_attendance(self, data: AttendanceCreate) -> AttendanceDetail:
        new_attendance = self.attendance_repo.create_attendance(
            lesson_id=data.lesson_id,
            student_id=data.student_id,
            is_present=data.is_present,
            reason=data.reason,
        )
        return AttendanceDetail.model_validate(new_attendance)

    def update_attendance(self, attendance_id: int, data: AttendanceUpdate) -> AttendanceDetail:
        attendance = self.attendance_repo.get_by_id(attendance_id)
        if attendance is None:
            raise ValueError("Ошибка: посещение не найдено!")
        updated = self.attendance_repo.update_attendance(
            attendance_id,
            is_present=data.is_present,
            reason=data.reason,
        )
        return AttendanceDetail.model_validate(updated)

    def delete_attendance(self, attendance_id: int) -> None:
        deleted = self.attendance_repo.delete_attendance(attendance_id)
        if not deleted:
            raise ValueError("Ошибка: посещение не найдено!")