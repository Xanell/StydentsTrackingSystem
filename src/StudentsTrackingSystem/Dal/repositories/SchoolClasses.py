from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from ..DTOs.SchoolClasses import SchoolClass

class SchoolClassesRepository:      # Репозиторий для работы с школьными классами

    def __init__(self, db: Session):
        self.db = db

    def create_class(self, number: int, letter: str, school_year_id: int) -> SchoolClass:

        """Создать класс"""

        school_class = SchoolClass(number = number, letter = letter.upper(), school_year_id = school_year_id)

        self.db.add(school_class)
        self.db.commit()
        self.db.refresh(school_class)

        return school_class

    def get_class_by_id(self, class_id: int) -> SchoolClass:

        """Получить класс по ID"""

        return self.db.get(SchoolClass, class_id)

    def get_all_classes(self) -> list[SchoolClass]:

        """Получить все классы"""

        stmt = select(SchoolClass).order_by(SchoolClass.number, SchoolClass.letter)

        return self.db.scalars(stmt).all()

    def get_classes_by_year(self, school_year_id: int) -> list[SchoolClass]:

        """Получить все классы учебного года"""

        stmt = (select(SchoolClass).where(SchoolClass.school_year_id == school_year_id).order_by(SchoolClass.number, SchoolClass.letter))

        return self.db.scalars(stmt).all()

    def delete_class(self, class_id: int) -> bool:

        """Удалить класс"""

        school_class = self.db.get(SchoolClass, class_id)
        
        self.db.delete(school_class)
        self.db.commit()

        return True

    