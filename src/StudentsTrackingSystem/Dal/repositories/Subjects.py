from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Subjects import Subjects


class SubjectsRepository:
    # Конструктор: принимает сессию БД и сохраняет её для дальнейшего использования
    def __init__(self, session: Session):
        self.session = session

    # Создаёт новый предмет и сохраняет его в БД, возвращает объект с присвоенным id
    def add_a_subject(self, name: str, description: str) -> Subjects:
        subject = Subjects(name=name, description=description)
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject

    # Ищет предмет по его id, возвращает объект или None, если не найден
    def get_by_id(self, subject_id: int) -> Subjects | None:
        stmt = select(Subjects).where(Subjects.id == subject_id)
        return self.session.scalars(stmt).one_or_none()

    # Ищет предмет по имени, возвращает объект или None, если не найден
    def get_by_name(self, name: str) -> Subjects | None:
        stmt = select(Subjects).where(Subjects.name == name)
        return self.session.scalars(stmt).one_or_none()

    # Возвращает список всех предметов из таблицы
    def get_all(self) -> list[Subjects]:
        return self.session.scalars(select(Subjects)).all()

    # Обновляет имя и/или описание предмета по id, возвращает обновлённый объект или None
    def update(self, subject_id: int, name: str | None = None, description: str | None = None) -> Subjects | None:
        subject = self.get_by_id(subject_id)
        # Нужны ли проверки ??
        if subject is None:
            return None
        if name is not None:
            subject.name = name
        if description is not None:
            subject.description = description
        self.session.commit()
        self.session.refresh(subject)
        return subject

    # Удаляет предмет по id, возвращает True если удалён, False если не найден
    def delete(self, subject_id: int) -> bool:
        subject = self.get_by_id(subject_id)
        if subject is None:
            return False
        self.session.delete(subject)
        self.session.commit()
        return True