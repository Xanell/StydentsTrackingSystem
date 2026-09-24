from Bll.Schemas.Base import BaseSchema
from pydantic import computed_field
from Core.Enums import RoleName, ROLE_LABELS

class UserRoleDetail(BaseSchema):
    id: int
    name: str

    @computed_field
    @property
    def label(self) -> str:
        """Русское название для UI."""
        return ROLE_LABELS.get(self.name, self.name)