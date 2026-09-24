from Bll.Schemas.Base import BaseSchema
from datetime import date

class SchoolYearDetail(BaseSchema):
    id: int
    name: str
    start_date: date
    end_date: date
    is_current: bool

class SchoolYearCreate(BaseSchema):
    start_date: date
    end_date: date

class SchoolYearUpdate(BaseSchema):
    start_date: date | None = None
    end_date: date | None = None