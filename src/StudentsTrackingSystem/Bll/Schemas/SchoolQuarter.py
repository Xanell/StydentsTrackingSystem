from Bll.Schemas.Base import BaseSchema
from datetime import date

class SchoolQuarterShort(BaseSchema):
    id: int
    number: int

class SchoolQuarterDetail(BaseSchema):
    id: int
    school_year_id: int
    number: int
    start_date: date
    end_date: date

class SchoolQuarterCreate(BaseSchema):
    school_year_id: int
    number: int
    start_date: date
    end_date: date

class SchoolQuarterUpdate(BaseSchema):
    start_date: date | None = None
    end_date: date | None = None