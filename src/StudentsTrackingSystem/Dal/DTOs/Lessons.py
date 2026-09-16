from .Base import Base
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

class Lessons(Base):
    __tablename__ = "Lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)
    topic: Mapped[str] = mapped_column(String(255))
    homework_description: Mapped[str] = mapped_column(String(255))
    homework_due_date: Mapped[date] = mapped_column(Date)
    files: Mapped[str] = mapped_column(String)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("Schedule.id"))

    schedule: Mapped[list["Schedule"]] = relationship(back_populates="lesson")
    results: Mapped[list["LessonsResults"]] = relationship(back_populates="lesson")
    attendances: Mapped[list["Attendance"]] = relationship(back_populates="lesson")
