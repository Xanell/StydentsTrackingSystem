from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.User import User
from ..DTOs.UserRole import UserRole

class UserRepository:
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
    def update_user(self, user_id: int ,username: str | None = None, password: str | None = None, first_name: str | None = None, last_name: str | None = None, middle_name: str | None = None, role_id: int | None = None, class_id: int | None = None) -> User | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        if username is not None:
            user.username = username
        if password is not None:
            user.password = password
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if middle_name is not None:
            user.middle_name = middle_name
        if role_id is not None:
            user.role_id = role_id
        if class_id is not None:
            user.class_id = class_id
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user is None:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalars(stmt).one_or_none()

    def get_by_role(self, role_name: str) -> list[User]:
        stmt = (select(User)
                .join(User.role)
                .where(UserRole.name == role_name)
                )
        return self.db.scalars(stmt).all()

    def clear_class(self, user_id: int) -> Users | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        user.class_id = None
        self.db.commit()
        self.db.refresh(user)
        return user