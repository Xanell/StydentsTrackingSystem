from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Attendance import Attendance

class AttendanceRepository:
    def __init__(self, session: Session):
        self.db = session

    def create_attendance(self, lesson_id: int, student_id: int, is_present: bool, reason: str | None) -> Attendance:
        new_attendance = Attendance(
            lesson_id = lesson_id,
            student_id = student_id,
            is_present = is_present,
            reason = reason
            )
        self.db.add(new_attendance)
        self.db.commit()
        self.db.refresh(new_attendance)

        return new_attendance

    def get_by_id(self, attendance_id: int) -> Attendance | None:
        return self.db.get(Attendance, attendance_id)

    def get_all(self) -> list[Attendance]:
        return self.db.scalars(select(Attendance)).all()

    def update_attendance(self, attendance: Attendance, **kwargs) -> Attendance:
        for key, value in kwargs.items():
            setattr(attendance, key, value)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def delete_attendance(self, attendance: Attendance) -> None:
        self.db.delete(attendance)
        self.db.commit()

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