from .Base import Base
from sqlalchemy import Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Schedule(Base):
    __tablename__ = "Schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("SchoolClasses.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("Subjects.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    period_id: Mapped[int] = mapped_column(ForeignKey("LessonsPeriods.id"))
    day_of_week: Mapped[int] = mapped_column(SmallInteger)
    room: Mapped[str] = mapped_column(String(10))

    school_class: Mapped["SchoolClasses"] = relationship(back_populates="schedule")
    subject: Mapped["Subjects"] = relationship(back_populates="schedule")
    teacher: Mapped["Users"] = relationship(back_populates="schedule")
    period: Mapped["LessonsPeriods"] = relationship(back_populates="schedule")
    lesson: Mapped["Lesson"] = relationship(back_populates="schedule")
