from .Base import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Attendance(Base):
    __tablename__ = "Attendances"
    __table_args__ = (
        UniqueConstraint("lesson_id", "student_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("Lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    is_present: Mapped[bool] = mapped_column(Boolean)
    reason: Mapped[str | None] = mapped_column(String(255))

    lesson: Mapped["Lesson"] = relationship(back_populates="attendances")
    student: Mapped["User"] = relationship(back_populates="attendances")