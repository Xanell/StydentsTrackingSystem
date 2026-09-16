from .Base import Base
from sqlalchemy import Integer, String, ForeignKey, SmallInteger, Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.StudentsTrackingSystem.Core.Enums import GradeType

class LessonsResults(Base):
    __tablename__ = "LessonsResults"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("Lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    file: Mapped[str] = mapped_column(String)
    grade: Mapped[int] = mapped_column(SmallInteger)
    grade_type: Mapped[GradeType] = mapped_column(Enum(
        GradeType,
        name="grade_type_enum"
    ))
    submited_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    lesson: Mapped["Lessons"] = relationship(back_populates="results")
    student: Mapped["Users"] = relationship(back_populates="lesson_results")