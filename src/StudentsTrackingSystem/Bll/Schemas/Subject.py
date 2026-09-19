from Bll.Schemas.Base import BaseSchema

class SubjectShort(BaseSchema):
    id: int
    name: str

class SubjectDetail(BaseSchema):
    id: int
    name: str
    description: str

class SubjectCreate(BaseSchema):
    name: str
    description: str

class SubjectUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None