from sqlalchemy.orm import Session
from Bll.Schemas.SchoolYear import SchoolYearCreate, SchoolYearDetail, SchoolYearShort
from Dal.repositories.SchoolYear import SchoolYearRepository

class SchoolYearService:
    def __init__(self, session: Session):
        self.school_year_repo = SchoolYearRepository(session)

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

    def get_by_id(self, year_id: int) -> SchoolYearDetail:
        year = self.school_year_repo.get_by_id(year_id)
        if year is None:
            raise ValueError("Ошибка!!")
        return SchoolYearDetail.model_validate(year)

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

    def delete_year(self, year_id: int) -> None:
        if not self.school_year_repo.delete_year(year_id):
            raise ValueError("Ошибка!!")
        