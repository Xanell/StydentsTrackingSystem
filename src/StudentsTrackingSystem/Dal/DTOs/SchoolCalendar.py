from .Base import Base
from sqlalchemy import Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from Core.Enums import DayType

class SchoolCalendar(Base):
    __tablename__ = "SchoolCalendar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year_id: Mapped[int] = mapped_column(ForeignKey("SchoolYear.id"))
    calendar_date: Mapped[date] = mapped_column(Date)
    day_type: Mapped[DayType] = mapped_column(Enum(
        DayType,
        name="day_type_enum"
    ))

    school_year: Mapped["SchoolYear"] = relationship(back_populates="school_calendar")