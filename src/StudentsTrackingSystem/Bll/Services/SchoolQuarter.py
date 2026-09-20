from datetime import date
from sqlalchemy.orm import Session
from Bll.Schemas.SchoolQuarter import SchoolQuarterCreate, SchoolQuarterDetail, SchoolQuarterShort, SchoolQuarterUpdate
from Dal.Repositories.SchoolQuarter import QuarterRepository
from Dal.Repositories.SchoolYear import SchoolYearRepository

class SchoolQuarterService:
    def __init__(self, session: Session):
        self.school_quarter_repo = QuarterRepository(session)
        self.school_year_repo = SchoolYearRepository(session)

    def create_quarter(self, data: SchoolQuarterCreate) -> SchoolQuarterDetail:
        year = self.school_year_repo.get_by_id(data.school_year_id)
        if year is None:
            raise ValueError(f"Год с id={data.school_year_id} не найден")

        if data.end_date <= data.start_date:
            raise ValueError("Дата окончания должна быть позже даты начала")

        if not (year.start_date <= data.start_date <= year.end_date):
            raise ValueError("Дата начала четверти вне границ учебного года")
        if not (year.start_date <= data.end_date <= year.end_date):
            raise ValueError("Дата окончания четверти вне границ учебного года")

        if self.school_quarter_repo.get_by_number(data.school_year_id, data.number) is not None:
            raise ValueError(f"Четверть с номером {data.number} уже существует в этом году")

        new_quarter = self.school_quarter_repo.create_quarter(
            school_year_id=data.school_year_id,
            number=data.number,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        return SchoolQuarterDetail.model_validate(new_quarter)

    def get_by_id(self, quarter_id: int) -> SchoolQuarterDetail:
        quarter = self.school_quarter_repo.get_by_id(quarter_id)

        if quarter is None:
            raise ValueError("Ошибка: четверть не найдена!")
        return SchoolQuarterDetail.model_validate(quarter)

    def get_all_quarters(self, year_id: int) -> list[SchoolQuarterDetail]:
        year = self.school_year_repo.get_by_id(year_id)
        if year is None:
            raise ValueError(f"Год с id={year_id} не найден")

        quarters = self.school_quarter_repo.get_by_year(year_id)
        result = []
        for quarter in quarters:
            result.append(SchoolQuarterDetail.model_validate(quarter))
        return result

    def get_current_quarter(self, year_id: int) -> SchoolQuarterDetail:
        curr_quarter = self.school_quarter_repo.get_by_date(year_id, date.today())

        if curr_quarter is None:
            raise ValueError("Ошибка: что - то не так!")
        return SchoolQuarterDetail.model_validate(curr_quarter)

    def update_quarter(self, quarter_id: int, data: SchoolQuarterUpdate) -> SchoolQuarterDetail:
        quarter = self.school_quarter_repo.get_by_id(quarter_id)
        if quarter is None:
            raise ValueError(f"Четверть с id={quarter_id} не найдена")

        new_start = data.start_date or quarter.start_date
        new_end = data.end_date or quarter.end_date

        if new_end <= new_start:
            raise ValueError("Дата окончания должна быть позже даты начала")

        year = self.school_year_repo.get_by_id(quarter.school_year_id)
        if year is None:
            raise ValueError(f"Год с id={quarter.school_year_id} не найден")

        if not (year.start_date <= new_start <= year.end_date):
            raise ValueError("Дата начала четверти вне границ учебного года")
        if not (year.start_date <= new_end <= year.end_date):
            raise ValueError("Дата окончания четверти вне границ учебного года")

        updated = self.school_quarter_repo.update_quarter(
            quarter_id,
            start_date=new_start,
            end_date=new_end,
        )
        return SchoolQuarterDetail.model_validate(updated)