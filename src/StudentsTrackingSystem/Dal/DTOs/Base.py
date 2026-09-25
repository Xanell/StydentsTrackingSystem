from enum import Enum as PyEnum

from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def str_enum(enum_cls: type[PyEnum], name: str) -> Enum:
    """
    Колонка для Python-enum'а из Core.Enums.
    В базе хранится обычная строка (VARCHAR) со значением ("admin", "test"...)
    и CHECK-ограничением. Новый вариант enum'а не требует ALTER TYPE.
    """
    return Enum(
        enum_cls,
        name=name,
        native_enum=False,
        create_constraint=True,
        length=20,
        values_callable=lambda e: [member.value for member in e],
    )
