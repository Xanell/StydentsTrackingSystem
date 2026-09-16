from .Base import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Users(Base): 
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25))
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(25))
    middle_name: Mapped[str] = mapped_column(String(25))
    role_id: Mapped[int] = mapped_column(ForeignKey("UserRole.id"))
    class_id : Mapped[int | None] = mapped_column(ForeignKey("SchoolClasses.id"))

    role: Mapped["UserRole"] = relationship(back_populates="users")
    school_class: Mapped["SchoolClasses | None"] = relationship(back_populates="students")
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="teacher")
    lesson_results: Mapped[list["LessonsResults"]] = relationship(back_populates="student")
    attendances: Mapped[list["Attendance"]] = relationship(back_populates="student")
