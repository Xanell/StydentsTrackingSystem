from .Base import Base
from sqlalchemy import Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SchoolClasses(Base):
    __tablename__ = "SchoolClasses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    letter: Mapped[str] = mapped_column(String(1), nullable=False)
    year_id: Mapped[int] = mapped_column(ForeignKey("SchoolYear.id"))

    students: Mapped[list["Users"]] = relationship(back_populates="school_class")
    school_year: Mapped["SchoolYear"] = relationship(back_populates="school_classes")
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="school_class")
