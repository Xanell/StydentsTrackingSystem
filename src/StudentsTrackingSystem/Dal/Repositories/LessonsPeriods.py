from datetime import time
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..DTOs.LessonsPeriods import LessonPeriod

class LessonsPeriodsRepository:     # Репозиторий для работы с разбивкой времени уроков

    def __init__(self, session: Session):
        self.db = session

    def create_period(self, start_time: time, end_time: time) -> LessonPeriod:

        new_period = LessonPeriod(
            start_time=start_time,
            end_time=end_time
            )
        
        self.db.add(new_period)
        self.db.commit()
        self.db.refresh(new_period)
        return new_period

    def get_by_id(self, period_id: int) -> LessonPeriod | None:
        return self.db.get(LessonPeriod, period_id)

    def get_all(self) -> list[LessonPeriod]:
        stmt = select(LessonPeriod).order_by(LessonPeriod.start_time)
        return self.db.scalars(stmt).all()

    def update_period(self, period_id: int, start_time: time | None = None, end_time: time | None = None) -> LessonPeriod | None:
        period = self.get_by_id(period_id)
        if period is None:
            return None
        if start_time is not None:
            period.start_time = start_time
        if end_time is not None:
            period.end_time = end_time
        self.db.commit()
        self.db.refresh(period)
        return period
    
    def delete_period(self, period_id: int) -> bool:
        period = self.get_by_id(period_id)
        if period is None:
            return False
        self.db.delete(period)
        self.db.commit()
        return True