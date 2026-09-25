from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class HomeworkSubmission(Base):
    """
    Сдача домашки. lesson_id — урок, на котором задание ЗАДАЛИ.
    Оценка за неё — Mark с тем же lesson_id и grade_type = HOMEWORK.

    Сдачи не удаляются и не перезаписываются: повторная сдача — это новая строка.
    Действующей считается последняя по submitted_at, предыдущие остаются как история попыток.
    """

    __tablename__ = "homework_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    file_path: Mapped[str] = mapped_column(String(255))
    original_name: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str | None] = mapped_column(String(500))
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    lesson: Mapped["Lesson"] = relationship(back_populates="submissions")
    student: Mapped["User"] = relationship(lazy="joined")
