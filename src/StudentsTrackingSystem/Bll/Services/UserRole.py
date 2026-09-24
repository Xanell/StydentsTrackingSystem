from sqlalchemy.orm import Session
from Bll.Schemas.UserRole import UserRoleDetail
from Dal.Repositories.UserRole import UserRoleRepository

class UserRoleService:
    def __init__(self, session: Session):
        self.role_repo = UserRoleRepository(session)

    def get_all(self) -> list[UserRoleDetail]:
        roles = self.role_repo.get_all()
        result = []
        for role in roles:
            result.append(UserRoleDetail.model_validate(role))
        return result