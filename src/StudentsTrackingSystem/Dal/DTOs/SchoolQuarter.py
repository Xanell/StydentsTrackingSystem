from .Base import Base
from sqlalchemy import ForeignKey, Integer, Date, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

class SchoolQuarter(Base):
    __tablename__ = "Quarters"
    __table_args__ = (
        UniqueConstraint("school_year_id", "number"),
        CheckConstraint("end_date > start_date"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    school_year_id: Mapped[int] = mapped_column(ForeignKey("SchoolYear.id"))
    number: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    school_year: Mapped["SchoolYear"] = relationship(back_populates="quarters")