from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.UserRole import UserRole

class UserRoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> UserRole | None:
        stmt = select(UserRole).where(UserRole.name == name)
        return self.session.scalar(stmt).one_or_none()
    
    # Метод получения списка всех ролей для UI
    def get_all(self) -> list[UserRole]:
        return list(self.session.scalar(select(UserRole)).all())