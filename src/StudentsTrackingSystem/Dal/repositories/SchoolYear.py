from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.SchoolYear import SchoolYear

class SchoolYearRepository:     # Репозиторий для работы с учебными годами

    def __init__(self, db: Session):
        self.db = db

    def create_schoolyear(self, name: str, start_date: date, end_date: date, is_current: bool = False) -> SchoolYear:

        """Создать учебный год"""

        school_year = SchoolYear(name = name, start_date = start_date, end_date = end_date, is_current = is_current)

        self.db.add(school_year)
        self.db.commit()
        self.db.refresh(school_year)

        return school_year

    def get_by_id(self, year_id: int) -> SchoolYear:

        """Получить школьный год по ID"""

        return self.db.get(SchoolYear, year_id)

    def get_by_name(self, name: str) -> SchoolYear:

        """Получить по названию"""

        stmt = select(SchoolYear).where(SchoolYear.name == name)

        return self.db.scalars(stmt).first()

    def get_all(self) -> list[SchoolYear]:

        """Получить все учебные годы"""

        stmt = select(SchoolYear).order_by(SchoolYear.start_date.desc())

        return list(self.db.scalars(stmt).all())

    def get_current(self) -> SchoolYear:

        """Получить текущий учебный год"""

        stmt = select(SchoolYear).where(SchoolYear.is_current == True)

        return self.db.scalars(stmt).first()

    def get_past_years(self) -> list[SchoolYear]:

        """Получить прошедшие учебные годы"""

        stmt = (select(SchoolYear).where(SchoolYear.end_date < date.today()).order_by(SchoolYear.end_date.desc()))

        return list(self.db.scalars(stmt).all())

    def delete_year(self, year_id: int) -> bool:

        """Удалить учебный год"""

        school_year = self.db.get(SchoolYear, year_id)

        if not school_year:
            return False
        
        self.db.delete(school_year)
        self.db.commit()

        return True

    
