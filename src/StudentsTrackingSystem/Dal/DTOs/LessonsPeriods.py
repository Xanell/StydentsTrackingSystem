from .Base import Base
from sqlalchemy import Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time

class LessonsPeriods(Base):
    __tablename__ = "LessonsPeriods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    schedule: Mapped[list["Schedule"]] = relationship(back_populates="period")
