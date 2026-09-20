from Bll.Schemas.Base import BaseSchema

class SchoolClassShort(BaseSchema):
    id: int
    number: int
    letter: str

class SchoolClassCreate(BaseSchema):
    number: int
    letter: str
    school_year_id: int

class SchoolClassUpdate(BaseSchema):
    number: int | None = None
    letter: str | None = None