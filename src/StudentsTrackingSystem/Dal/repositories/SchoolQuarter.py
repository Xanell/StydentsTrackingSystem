from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.SchoolQuarter import SchoolQuarter
from datetime import date

class QuarterRepository:
    def __init__(self, session: Session):
        self.db = session

    def create_quarter(self, school_year_id: int, number: int, start_date: date, end_date: date) -> SchoolQuarter:
        new_quarter = SchoolQuarter(
            school_year_id=school_year_id,
            number=number,
            start_date=start_date,
            end_date=end_date
        )
        self.db.add(new_quarter)
        self.db.commit()
        self.db.refresh(new_quarter)
        return new_quarter

    def get_by_id(self, quarter_id: int) -> SchoolQuarter | None:
        return self.db.get(SchoolQuarter, quarter_id)

    def get_all(self) -> list[SchoolQuarter]:
        stmt = select(SchoolQuarter).order_by(SchoolQuarter.number)
        return self.db.scalars(stmt).all()

    def get_by_year(self, year_id: int) -> list[SchoolQuarter]:
        stmt = select(SchoolQuarter).where(SchoolQuarter.school_year_id == year_id)
        return self.db.scalars(stmt).all()

    def get_by_number(self, year_id: int, number: int) -> SchoolQuarter | None:
        stmt = select(SchoolQuarter).where(SchoolQuarter.school_year_id == year_id, SchoolQuarter.number == number)
        return self.db.scalars(stmt).one_or_none()

    def get_by_date(self, year_id: int, target_date: date) -> SchoolQuarter | None:
        stmt = select(SchoolQuarter).where(SchoolQuarter.school_year_id == year_id, SchoolQuarter.start_date <= target_date, SchoolQuarter.end_date >= target_date)
        return self.db.scalars(stmt).one_or_none()

    def update_quarter(self, quarter_id: int, start_date: date | None = None, end_date: date | None = None) -> SchoolQuarter | None:
        quarter = self.get_by_id(quarter_id)
        if quarter is None:
            return None
        if start_date is not None:
            quarter.start_date = start_date
        if end_date is not None:
            quarter.end_date = end_date
        self.db.commit()
        self.db.refresh(quarter)
        return quarter

    def delete_quarter(self, quarter_id: int) -> bool:
        quarter = self.get_by_id(quarter_id)
        if quarter is None:
            return False
        self.db.delete(quarter)
        self.db.commit()
        return True