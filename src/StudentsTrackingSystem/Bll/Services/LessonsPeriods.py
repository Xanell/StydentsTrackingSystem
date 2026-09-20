from sqlalchemy.orm import Session
from Bll.Schemas.LessonsPeriods import LessonPeriodCreate, LessonPeriodDetail, LessonPeriodUpdate
from Dal.Repositories.LessonsPeriods import LessonsPeriodsRepository

class LessonsPeriodsService:
    def __init__(self, session: Session):
        self.period_repo = LessonsPeriodsRepository(session)

    def create_period(self, data: LessonPeriodCreate) -> LessonPeriodDetail:

        if data.start_time >= data.end_time:
            raise ValueError("Ошибка: Время начала должна быть раньше времени окончания!")
        # возможно cюда еще надо добавить проверки на пересечение с другими периодами и уникальность начала start_time
        new_period = self.period_repo.create_period(start_time=data.start_time, end_time=data.end_time)
        return LessonPeriodDetail.model_validate(new_period)

    def get_by_id(self, period_id: int) -> LessonPeriodDetail:

        period = self.period_repo.get_by_id(period_id)

        if period is None:
            raise ValueError("Ошибка: не найден!")

        return LessonPeriodDetail.model_validate(period)

    def get_all_periods(self) -> list[LessonPeriodDetail]:

        all_periods = self.period_repo.get_all()
        result = []

        for period in all_periods:
             result.append(LessonPeriodDetail.model_validate(period))
        return result   

    def update_period(self, period_id: int, data: LessonPeriodUpdate) -> LessonPeriodDetail:
        period = self.period_repo.get_by_id(period_id)

        if period is None:
            raise ValueError("Ошибка: период не найден!")

        new_start_time = data.start_time if data.start_time is not None else period.start_time
        new_end_time = data.end_time if data.end_time is not None else period.end_time

        if new_start_time >= new_end_time:
            raise ValueError("Ошибка: Время начала не может быть раньше времени окончания!")

        # тоже возможно cюда еще надо добавить проверки на пересечение с другими периодами и уникальность начала start_time

        update_period = self.period_repo.update_period(period_id, start_time=new_start_time, end_time=new_end_time)

        return LessonPeriodDetail.model_validate(update_period)
        

    
        
                
                
                    
