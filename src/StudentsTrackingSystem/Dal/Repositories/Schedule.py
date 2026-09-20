from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Schedule import Schedule

class ScheduleRepository:       # Репозиторий для работы с расписанием

    def __init__(self, session: Session):
        self.db = session

    """Создать расписание"""

    def create_schedule(self,
        class_id: int,
        subject_id: int,
        teacher_id: int,
        period_id: int,
        day_of_week: int,
        room: str
        ) -> Schedule:

        schedule = Schedule(
            class_id=class_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            period_id=period_id,
            day_of_week=day_of_week,
            room=room
        )

        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)

        return schedule

    def get_schedule_by_id(self, schedule_id: int) -> Schedule | None:

        """Получить по ID"""

        return self.db.get(Schedule, schedule_id)

    def get_all_schedule(self) -> list[Schedule]:

        """Получить все записи"""

        stmt = select(Schedule).order_by(Schedule.day_of_week, Schedule.period_id)

        return self.db.scalars(stmt).all()

    def get_schedule_by_class(self, class_id: int) -> list[Schedule]:

        """Получить расписание класса"""

        stmt = (select(Schedule).where(Schedule.class_id == class_id).order_by(Schedule.day_of_week, Schedule.period_id))

        return self.db.scalars(stmt).all()

    def get_schedule_by_teacher(self, teacher_id: int) -> list[Schedule]:

        """Получить расписание учителя"""

        stmt = (select(Schedule).where(Schedule.teacher_id == teacher_id).order_by(Schedule.day_of_week, Schedule.period_id))

        return self.db.scalars(stmt).all()

    def update_schedule(
        self,
        schedule_id: int,
        subject_id: int | None = None,
        teacher_id: int | None = None,
        room: str | None = None,
        day_of_week: int | None = None,
        ) -> Schedule | None:
    
        schedule = self.get_schedule_by_id(schedule_id)
        if schedule is None:
            return None

        if subject_id is not None:
            schedule.subject_id = subject_id
        if teacher_id is not None:
            schedule.teacher_id = teacher_id
        if room is not None:
            schedule.room = room
        if day_of_week is not None:
            schedule.day_of_week = day_of_week

        self.db.commit()
        self.db.refresh(schedule)
        return schedule

    def delete_schedule(self, schedule_id: int) -> bool:
        schedule = self.get_schedule_by_id(schedule_id)
        if schedule is None:
            return False
        self.db.delete(schedule)
        self.db.commit()
        return True