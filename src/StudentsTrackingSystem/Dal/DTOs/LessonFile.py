from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class LessonFile(Base):
    """
    Материал к уроку. Сам файл лежит в MEDIA_ROOT, здесь только путь и исходное имя.
    Не удаляется: если прикрепили не тот файл, его открепляют (detached_at),
    и он перестаёт показываться у урока. Файл на диске тоже остаётся.
    """

    __tablename__ = "lesson_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    file_path: Mapped[str] = mapped_column(String(255))      # "lessons/3f2a…c1.pdf"
    original_name: Mapped[str] = mapped_column(String(255))  # "Дроби_презентация.pdf"
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    detached_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # None — прикреплён

    lesson: Mapped["Lesson"] = relationship()
