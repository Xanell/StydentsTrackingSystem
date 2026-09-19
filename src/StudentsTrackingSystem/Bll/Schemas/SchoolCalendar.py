from Bll.Schemas.Base import BaseSchema
from datetime import date
from Core.Enums import DayType

class SchoolCalendarDetail(BaseSchema):
    id: int
    year_id: int
    calendar_date: date
    day_type: DayType

class SchoolCalendarUpdate(BaseSchema):
    day_type: DayType