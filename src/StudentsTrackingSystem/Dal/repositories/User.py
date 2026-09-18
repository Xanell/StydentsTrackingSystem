from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.User import User
from ..DTOs.UserRole import UserRole

class UserRepository():
    def __init__(self, session: Session):
        self.db = session

    def create_user(self, username: str, password: str, first_name: str, last_name: str,middle_name: str, role_id: int, class_id: int | None) -> Users:
        new_user = User(
            username = username, 
            password = password, 
            first_name = first_name, 
            last_name = last_name, 
            middle_name = middle_name, 
            role_id = role_id, 
            class_id = class_id
            )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_all(self) -> list[User]:
        return self.db.scalars(select(User)).all()

    # Переделать на конкретные аргументы 
    def update_user(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalars(stmt).one_or_none()

    def get_by_role(self, role_name: str) -> list[User]:
        stmt = (select(User)
                .join(User.role)
                .where(UserRole.name == role_name)
                )
        return self.db.scalars(stmt).all()