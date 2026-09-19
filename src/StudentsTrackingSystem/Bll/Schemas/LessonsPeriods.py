from Bll.Schemas.Base import BaseSchema
from datetime import time

class LessonPeriodDetail(BaseSchema):
    id: int
    start_time: time
    end_time: time

class LessonPeriodCreate(BaseSchema):
    start_time: time
    end_time: time

class LessonPeriodUpdate(BaseSchema):
    start_time: time | None = None
    end_time: time | None = None
