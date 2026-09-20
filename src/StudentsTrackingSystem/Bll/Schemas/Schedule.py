from Bll.Schemas.Base import BaseSchema
from Bll.Schemas.User import UserShort   # ← импорт user, но user не импортирует schedule
from Bll.Schemas.Subject import SubjectShort
from Bll.Schemas.SchoolClasses import SchoolClassShort
from Bll.Schemas.LessonsPeriods import LessonPeriodDetail

class ScheduleDetail(BaseSchema):
    id: int
    day_of_week: int
    room: str
    teacher: UserShort
    subject: SubjectShort
    school_class: SchoolClassShort
    period: LessonPeriodDetail

class ScheduleCreate(BaseSchema):
    class_id: int
    subject_id: int    
    teacher_id: int    
    period_id: int   
    day_of_week: int   
    room: str

class ScheduleUpdate(BaseSchema):
    subject_id: int | None = None
    teacher_id: int | None = None
    room: str | None = None
    day_of_week: int | None = None