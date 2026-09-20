from sqlalchemy.orm import Session
from Bll.Schemas.SchoolYear import SchoolYearCreate, SchoolYearDetail, SchoolYearShort, SchoolYearUpdate
from Dal.Repositories.SchoolYear import SchoolYearRepository
from Dal.Repositories.SchoolCalendar import SchoolCalendarRepository
from Dal.Repositories.SchoolQuarter import QuarterRepository

class SchoolYearService:
    def __init__(self, session: Session):
        self.school_year_repo = SchoolYearRepository(session)
        self.school_calendar_repo = SchoolCalendarRepository(session)
        self.school_quarter_repo = QuarterRepository(session)

    def create_school_year(self, data: SchoolYearCreate) -> SchoolYearDetail:
        start_date = data.start_date
        end_date = data.end_date

        if end_date <= start_date:
            raise ValueError("Ошибка!!")

        year_name = f"{start_date.year}/{end_date.year}"
        if self.school_year_repo.get_by_name(year_name) is not None:
            raise ValueError("Ошибка такой год уже есть!")

        new_year = self.school_year_repo.create_school_year(name=year_name, start_date=start_date, end_date=end_date, is_current=False)
        return SchoolYearDetail.model_validate(new_year)
    
    def update_year(self, year_id: int, data: SchoolYearUpdate) -> SchoolYearDetail:
        year = self.school_year_repo.get_by_id(year_id)
        if year is None:
            raise ValueError(f"Год с id={year_id} не найден")

        new_start = data.start_date or year.start_date
        new_end = data.end_date or year.end_date

        # Проверка: даты корректны
        if new_end <= new_start:
            raise ValueError("Дата окончания должна быть позже даты начала")

        # Если меняются границы — календарь должен быть пустым
        bounds_changed = (new_start != year.start_date) or (new_end != year.end_date)
        if bounds_changed:
            if self.school_calendar_repo.get_by_year(year_id):
                raise ValueError("Нельзя менять границы года: сначала удалите календарь")

            for quarter in self.school_quarter_repo.get_by_year(year_id):
                if quarter.start_date < new_start or quarter.end_date > new_end:
                    raise ValueError(f"Четверть {quarter.number} выходит за новые границы года")
        
        new_name = f"{new_start.year}/{new_end.year}"
        if new_name != year.name:
            existing = self.school_year_repo.get_by_name(new_name)
            if existing is not None and existing.id != year_id:
                raise ValueError(f"Год '{new_name}' уже существует")

        updated = self.school_year_repo.update_year(
            year_id,
            start_date=new_start,
            end_date=new_end,
            name=new_name,
        )
        if updated is None:
            raise ValueError(f"Год с id={year_id} не найден")

        return SchoolYearDetail.model_validate(updated)  
      
    def get_by_id(self, year_id: int) -> SchoolYearDetail:
        curr_year = self.school_year_repo.get_by_id(year_id)
        if curr_year is None:
            raise ValueError("Ошибка!!")
        return SchoolYearDetail.model_validate(curr_year)

    def get_all(self) -> list[SchoolYearShort]:
        year_list = self.school_year_repo.get_all()
        result = []
        for year in year_list:
            result.append(SchoolYearShort.model_validate(year))
        return result

    def get_current(self) -> SchoolYearDetail | None:
        curr_year = self.school_year_repo.get_current()
        if curr_year is None:
            return None
        return SchoolYearDetail.model_validate(curr_year)

    def make_current(self, year_id: int) -> SchoolYearDetail:
        curr_year = self.school_year_repo.get_by_id(year_id)
        if curr_year is None:
            raise ValueError("Ошибка!!")
        if curr_year.is_current:
            return SchoolYearDetail.model_validate(curr_year)

        for year in self.school_year_repo.get_all():
            if year.is_current and year.id != year_id:
                self.school_year_repo.set_current(year.id, False)

        self.school_year_repo.set_current(curr_year.id, True)
        return SchoolYearDetail.model_validate(curr_year)
