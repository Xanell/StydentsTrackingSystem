from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Core.Enums import DayType
from .Base import Base, str_enum


class DayOff(Base):
    """
    Исключения из обычного календаря, которые нельзя вычислить:
    праздники, карантин, доп. каникулы, рабочая суббота (day_type = SCHOOL_DAY).
    Выходные (по дню недели) и каникулы между четвертями здесь не хранятся.
    Один день: start_date == end_date.

    Запись имеет приоритет над вычисленным типом дня.
    Не удаляется: ошибочный праздник переключают в SCHOOL_DAY.
    """

    __tablename__ = "days_off"
    __table_args__ = (
        CheckConstraint("end_date >= start_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_year_id: Mapped[int] = mapped_column(ForeignKey("school_years.id"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    day_type: Mapped[DayType] = mapped_column(str_enum(DayType, "day_type"))
    title: Mapped[str] = mapped_column(String(100))  # "День народного единства"

    school_year: Mapped["SchoolYear"] = relationship(back_populates="days_off")
