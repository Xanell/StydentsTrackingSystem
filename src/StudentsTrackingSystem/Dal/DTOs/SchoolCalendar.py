from .Base import Base
from sqlalchemy import Integer, ForeignKey, SmallInteger, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from src.StudentsTrackingSystem.Core.Enums import DayType

class SchoolCalendar(Base):
    __tablename__ = "SchoolCalendar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year_id: Mapped[int] = mapped_column(ForeignKey("SchoolYear.id"))
    date: Mapped[date] = mapped_column(Date)
    quarter: Mapped[int] = mapped_column(SmallInteger)
    day_type: Mapped[DayType] = mapped_column(Enum(
        DayType,
        name="day_type_enum"
    ))

    school_year: Mapped["SchoolYear"] = relationship(back_populates="school_calendar")