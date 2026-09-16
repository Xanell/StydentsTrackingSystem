from .Base import Base
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class LessonsPeriods(Base):
    __tablename__ = "LessonsPeriods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    schedule: Mapped[list["Schedule"]] = relationship(back_populates="period")
