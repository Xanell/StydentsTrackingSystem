from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Core.Enums import MAX_LESSONS_PER_DAY
from .Base import Base


class Schedule(Base):
    """
    Шаблон недели: что у класса стоит в понедельник 3-м уроком.
    Проведённые уроки хранятся отдельно в lessons и от этой таблицы не зависят.

    Занятость учителя (не два класса в один слот) проверяет сервис через
    ScheduleRepository.get_teacher_slot: ограничением в базе этого не сделать,
    потому что расписания прошлых лет тоже лежат здесь.
    """

    __tablename__ = "schedule"
    __table_args__ = (
        UniqueConstraint("class_id", "weekday", "lesson_number"),
        CheckConstraint("weekday BETWEEN 1 AND 7"),
        CheckConstraint(f"lesson_number BETWEEN 1 AND {MAX_LESSONS_PER_DAY}"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    weekday: Mapped[int] = mapped_column(SmallInteger)        # 1 — понедельник, как date.isoweekday()
    lesson_number: Mapped[int] = mapped_column(SmallInteger)  # ключ в Core.Enums.LESSON_TIMES
    room: Mapped[str | None] = mapped_column(String(10))

    school_class: Mapped["SchoolClass"] = relationship(lazy="joined")
    subject: Mapped["Subject"] = relationship(lazy="joined")
    teacher: Mapped["User"] = relationship(lazy="joined")
