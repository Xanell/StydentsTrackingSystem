from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Attendance import Attendance

class AttendanceRepository:
    def __init__(self, session: Session):
        self.db = session

    def create_attendance(self, lesson_id: int, student_id: int, is_present: bool, reason: str | None = None) -> Attendance:
        new_attendance = Attendance(
            lesson_id=lesson_id,
            student_id=student_id,
            is_present=is_present,
            reason=reason
            )
        self.db.add(new_attendance)
        self.db.commit()
        self.db.refresh(new_attendance)

        return new_attendance

    def get_by_id(self, attendance_id: int) -> Attendance | None:
        return self.db.get(Attendance, attendance_id)

    def get_all(self) -> list[Attendance]:
        return self.db.scalars(select(Attendance)).all()

    def update_attendance(self, attendance_id: int, is_present: bool | None = None, reason: str | None = None) -> Attendance | None:
        attendance = self.get_by_id(attendance_id)
        if attendance is None:
            return None
        if is_present is not None:
            attendance.is_present = is_present
        if reason is not None:
            attendance.reason = reason
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def delete_attendance(self, attendance_id: int) -> bool:
        attendance = self.get_by_id(attendance_id)
        if attendance is None:
            return False
        self.db.delete(attendance)
        self.db.commit()
        return True

    def get_by_lesson(self, lesson_id: int) -> list[Attendance]:
        stmt = select(Attendance).where(Attendance.lesson_id == lesson_id)
        return self.db.scalars(stmt).all()

    def get_by_lesson_and_student(self, lesson_id: int, student_id: int) -> Attendance | None:
        stmt = (
            select(Attendance)
            .where(
                Attendance.lesson_id == lesson_id,
                Attendance.student_id == student_id
            )
        )
        return self.db.scalars(stmt).one_or_none()