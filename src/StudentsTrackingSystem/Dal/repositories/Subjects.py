from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.Subjects import Subject

class SubjectsRepository:
    # Конструктор: принимает сессию БД и сохраняет её для дальнейшего использования
    def __init__(self, session: Session):
        self.db = session

    # Создаёт новый предмет и сохраняет его в БД, возвращает объект с присвоенным id
    def add_a_subject(self, name: str, description: str) -> Subject:
        subject = Subject(name=name, description=description)
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject

    # Ищет предмет по его id, возвращает объект или None, если не найден
    def get_by_id(self, subject_id: int) -> Subject | None:
        stmt = select(Subject).where(Subject.id == subject_id)
        return self.db.scalars(stmt).one_or_none()

    # Ищет предмет по имени, возвращает объект или None, если не найден
    def get_by_name(self, name: str) -> Subject | None:
        stmt = select(Subject).where(Subject.name == name)
        return self.db.scalars(stmt).one_or_none()

    # Возвращает список всех предметов из таблицы
    def get_all(self) -> list[Subject]:
        return self.db.scalars(select(Subject)).all()

    # Обновляет имя и/или описание предмета по id, возвращает обновлённый объект или None
    def update(self, subject_id: int, name: str | None = None, description: str | None = None) -> Subject | None:
        subject = self.get_by_id(subject_id)
        # Нужны ли проверки ??
        if subject is None:
            return None
        if name is not None:
            subject.name = name
        if description is not None:
            subject.description = description
        self.db.commit()
        self.db.refresh(subject)
        return subject

    # Удаляет предмет по id, возвращает True если удалён, False если не найден
    def delete(self, subject_id: int) -> bool:
        subject = self.get_by_id(subject_id)
        if subject is None:
            return False
        self.db.delete(subject)
        self.db.commit()
        return True