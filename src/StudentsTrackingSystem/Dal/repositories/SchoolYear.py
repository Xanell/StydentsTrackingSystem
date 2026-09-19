from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.SchoolYear import SchoolYear

class SchoolYearRepository:     # Репозиторий для работы с учебными годами

    def __init__(self, session: Session):
        self.db = session

    def create_school_year(self, name: str, start_date: date, end_date: date, is_current: bool = False) -> SchoolYear:

        """Создать учебный год"""

        school_year = SchoolYear(
            name=name, 
            start_date=start_date, 
            end_date=end_date, 
            is_current=is_current
        )

        self.db.add(school_year)
        self.db.commit()
        self.db.refresh(school_year)

        return school_year

    def get_by_id(self, year_id: int) -> SchoolYear | None:

        """Получить школьный год по ID"""

        return self.db.get(SchoolYear, year_id)

    def get_by_name(self, name: str) -> SchoolYear | None:

        """Получить по названию"""

        stmt = select(SchoolYear).where(SchoolYear.name == name)

        return self.db.scalars(stmt).one_or_none()

    def get_all(self) -> list[SchoolYear]:

        """Получить все учебные годы"""

        stmt = select(SchoolYear).order_by(SchoolYear.start_date.desc())

        return self.db.scalars(stmt).all()

    def get_current(self) -> SchoolYear | None:

        """Получить текущий учебный год"""

        stmt = select(SchoolYear).where(SchoolYear.is_current == True)

        return self.db.scalars(stmt).one_or_none()

    def get_past_years(self) -> list[SchoolYear]:

        """Получить прошедшие учебные годы"""

        stmt = (select(SchoolYear).where(SchoolYear.end_date < date.today()).order_by(SchoolYear.end_date.desc()))

        return self.db.scalars(stmt).all()

    def set_current(self, year_id: int, is_current: bool) -> SchoolYear | None:
        year = self.get_by_id(year_id)
        if year is None:
            return None
        year.is_current = is_current
        self.db.commit()
        self.db.refresh(year)
        return year

    def update_year(self, year_id: int, start_date: date | None = None, end_date: date | None = None, name: str | None = None) -> SchoolYear | None:
        year = self.get_by_id(year_id)
        if year is None:
            return None
        if start_date is not None:
            year.start_date = start_date
        if end_date is not None:
            year.end_date = end_date
        if name is not None:
            year.name = name
        self.db.commit()
        self.db.refresh(year)
        return year

