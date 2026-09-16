from .Base import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Attendance(Base):
    __tablename__ = "Attendances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("Lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    is_present: Mapped[bool] = mapped_column(Boolean)
    reason: Mapped[str] = mapped_column(String(255))

    lesson: Mapped["Lessons"] = relationship(back_populates="attendances")
    student: Mapped["Users"] = relationship(back_populates="attendances")