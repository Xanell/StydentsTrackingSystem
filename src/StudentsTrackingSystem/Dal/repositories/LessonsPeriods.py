from datetime import time
from sqlalchemy.orm import Session
from sqlalchemy import 

from ..DTOs.LessonsPeriods import LessonsPeriods


class LessonsPeriodsRepository:     # Репозиторий для работы с разбивкой времени уроков"""

    def __init__(self, db: Session):
        self.db = db


    def create_periods(self) -> list[LessonsPeriods]:

        """Периоды на 7 уроков"""

        periods = [
            {"start_time": time(8, 30), "end_time": time(9, 15)},
            {"start_time": time(9, 25), "end_time": time(10, 10)},
            {"start_time": time(10, 25), "end_time": time(11, 10)},
            {"start_time": time(11, 25), "end_time": time(12, 10)},
            {"start_time": time(12, 25), "end_time": time(13, 10)},
            {"start_time": time(13, 20), "end_time": time(14, 5)},
            {"start_time": time(14, 15), "end_time": time(15, 0)},
        ]

        return periods