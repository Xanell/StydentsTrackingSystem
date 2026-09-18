from .Base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Subject(Base):
    __tablename__ = "Subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))

    schedule: Mapped[list["Schedule"]] = relationship(back_populates="subject")