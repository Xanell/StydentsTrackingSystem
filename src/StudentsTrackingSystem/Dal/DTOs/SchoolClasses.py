from .Base import Base
from sqlalchemy import Integer, String, ForeignKey, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SchoolClass(Base):
    __tablename__ = "SchoolClasses"
    __table_args__ = (
        UniqueConstraint(
            "school_year_id", "number", "letter"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    letter: Mapped[str] = mapped_column(String(1), nullable=False)
    school_year_id: Mapped[int] = mapped_column(ForeignKey("SchoolYear.id"))

    students: Mapped[list["User"]] = relationship(back_populates="school_class")
    school_year: Mapped["SchoolYear"] = relationship(back_populates="school_classes")
    schedules: Mapped[list["Schedule"]] = relationship(back_populates="school_class")
