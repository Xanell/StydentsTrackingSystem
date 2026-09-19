from datetime import date
from sqlalchemy.orm import Session
from Bll.Schemas.SchoolQuarter import SchoolQuarterCreate, SchoolQuarterDetail, SchoolQuarterShort, SchoolQuarterUpdate
from Dal.repositories.SchoolQuarter import QuarterRepository
from Dal.repositories.SchoolYear import SchoolYearRepository

class SchoolQuarterService:
    def __init__(self, session: Session):

        self.schoolquarter_repo = QuarterRepository(session)
        self.schoolyear_repo = SchoolYearRepository(session)

    def create_quarter(self, quarter: SchoolQuarterCreate) -> SchoolQuarterDetail:

        new_quarter = self.schoolquarter_repo.create_quarter(
        school_year_id=quarter.school_year_id,
        number=quarter.number,
        start_date=quarter.start_date,
        end_date=quarter.end_date,
        )
      
        if quarter.end_date <= quarter.start_date:
            raise ValueError ("Ошибка: Дата начала позже даты окончания!")

        return SchoolQuarterDetail.model_validate(new_quarter)

    def get_by_id(self, quarter_id: int) -> SchoolQuarterDetail:

        quarter = self.schoolquarter_repo.get_by_id(quarter_id)

        if quarter is None:
            raise ValueError("Ошибка: четверть не найдена!")
        return SchoolQuarterDetail.model_validate(quarter)

    def get_all_quarters(self, year_id: int) -> SchoolQuarterDetail:

        all_quarters = self.scgoolyear_repo.get_by_id(year_id)

        if all_quarters is None:
            raise ValueError("Ошибка: Учебный год не найден!")
        return SchoolQuarterDetail.model_validate(all_quarters)

    def get_current_quarter(self, year_id: int) -> SchoolQuarterDetail:

        curr_quarter = self.schoolquarter_repo.get_by_date(year_id, date.today())

        if curr_quarter is None:
            raise ValueError("Ошибка: что - то не так!")
        return SchoolQuarterDetail.model_validate(curr_quarter)

    def update_quarter(self, quarter_id: int, quarter: SchoolQuarterUpdate) -> SchoolQuarterDetail:

        qua = self.schoolquarter_repo.get_by_id(quarter_id)

        if qua is None:
            raise ValueError("Ошибка: четверть не найдена!")

        if quarter.end_date <= quarter.start_date:
            raise ValueError("Ошибка: Дата начала позже даты окончания!")

        new_start_date = quarter.start_date
        new_end_date = quarter.end_date
        year = self.schoolyear_repo.get_by_id(quarter.school_year_id)

        if year is None:
            raise ValueError("Учебный год не найден")

        if not (year.start_date <= new_start_date <= year.end_date):
            raise ValueError(f"Ошибка! Дата начала вне учебного года!")
        
        if not (year.start_date <= new_end_date <= year.end_date):
            raise ValueError(f"Ошибка! Дата окончания вне учебного года!")

        update = self.schoolquarter_repo.update_quarter(quarter_id, quarter.start_date, quarter.end_date)

        return SchoolQuarterUpdate.model_validate(update)

    def delete_quarter(self, quarter_id: int) -> None:

        if not self.delete_quarter(quarter_id):
            raise ValueError(f"Ошибка! Четверть не найдена")