from datetime import time
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..DTOs.LessonsPeriods import LessonPeriod

class LessonsPeriodsRepository:     # Репозиторий для работы с разбивкой времени уроков

    def __init__(self, db: Session):
        self.db = db

    def add_period(self, start_time: time, end_time: time) -> LessonPeriod:

        new_period = LessonPeriod(
            start_time = start_time,
            end_time = end_time
            )
        
        self.db.add(new_period)
        self.db.commit()
        self.db.refresh(new_period)
        return new_period

    def get_by_id(self, period_id: int) -> LessonPeriod | None:
        return self.db.get(LessonPeriod, period_id)

    def get_all(self) ->  list[LessonPeriod]:
        return self.db.scalars(select(LessonPeriod)).all()
    # Изменить на конкретные аргументы
    def update_period(self, period: LessonPeriod, **kwargs) -> LessonPeriod:
        for key, value in kwargs.items():
            setattr(period, key, value)
        self.db.commit()
        self.db.refresh(period)
        return period
    
    def delete_period(self, period: LessonPeriod) -> None:
        self.db.delete(period)
        self.db.commit()