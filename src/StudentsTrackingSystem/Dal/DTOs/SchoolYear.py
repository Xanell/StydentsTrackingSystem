from .Base import Base
from sqlalchemy import Integer, String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

class SchoolYear(Base):
    __tablename__ = "SchoolYear"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)

    school_classes: Mapped[list["SchoolClasses"]] = relationship(back_populates="school_year")
    school_calendar: Mapped[list["SchoolCalendar"]] = relationship(back_populates="school_year")