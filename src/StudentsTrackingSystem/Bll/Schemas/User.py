from Bll.Schemas.Base import BaseSchema
from Bll.Schemas.UserRole import UserRoleDetail
from Bll.Schemas.SchoolClass import SchoolClassShort

class UserShort(BaseSchema):
    id: int
    username: str
    first_name: str
    middle_name: str
    last_name: str

class UserDetail(BaseSchema):
    id: int
    username: str
    first_name: str
    middle_name: str
    last_name: str
    role: UserRoleDetail
    school_class: SchoolClassShort | None

class UserCreate(BaseSchema):
    first_name: str
    middle_name: str
    last_name: str
    role_id: int
    class_id: int | None = None

class UserCreatedResponse(BaseSchema):
    id: int
    username: str
    password: str

class UserUpdate(BaseSchema):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    class_id: int | None = None