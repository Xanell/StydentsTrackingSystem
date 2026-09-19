from Bll.Schemas.Base import BaseSchema
from datetime import date

class SchoolYearShort(BaseSchema):
    id: int
    name: str
    is_current: bool

class SchoolYearDetail(BaseSchema):
    id: int
    name: str
    start_date: date
    end_date: date
    is_current: bool

class SchoolYearCreate(BaseSchema):
    start_date: date
    end_date: date
