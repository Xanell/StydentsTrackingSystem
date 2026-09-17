from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.UserRole import UserRole

class UserRoleRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_by_name(self, name: str) -> UserRole | None:
        stmt = select(UserRole).where(UserRole.name == name)
        return self.db.scalars(stmt).one_or_none()

    # Метод для проверки переданной роли на случай изменения данных пользователя
    def get_by_id(self, role_id: int) -> UserRole | None:
        return self.db.get(UserRole, role_id)
    
    # Метод получения списка всех ролей для UI
    def get_all(self) -> list[UserRole]:
        return self.db.scalars(select(UserRole)).all()