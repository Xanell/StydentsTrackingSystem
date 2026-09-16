from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.User import Users

class UserRepository():
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str, first_name: str, last_name: str,middle_name: str, role_id: int, class_id: int | None) -> Users:
        