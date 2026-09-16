from .Base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserRole(Base):
    __tablename__ = "UserRole"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)
    
    users: Mapped[list["Users"]] = relationship(back_populates="role")