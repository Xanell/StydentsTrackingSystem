from .Base import Base
from sqlalchemy import Integer, Time, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time

class LessonPeriod(Base):
    __tablename__ = "LessonsPeriods"
    __table_args__ = (
        UniqueConstraint(
            "start_time"
        ),
        CheckConstraint(
            "start_time < end_time"
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    schedule: Mapped[list["Schedule"]] = relationship(back_populates="period")
