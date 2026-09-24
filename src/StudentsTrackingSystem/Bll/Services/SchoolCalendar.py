from sqlalchemy.orm import Session
from Bll.Schemas.SchoolCalendar import SchoolCalendarDetail, SchoolCalendarUpdate
from Dal.Repositories.SchoolCalendar import SchoolCalendarRepository
from Dal.Repositories.SchoolYear import SchoolYearRepository
from datetime import timedelta, date
from Core.Enums import DayType
from Core.Exceptions import NotFoundError, ConflictError

class SchoolCalendarService:
    def __init__(self, session: Session):
        self.school_calendar_repo = SchoolCalendarRepository(session)
        self.school_year_repo = SchoolYearRepository(session)

    def generate_calendar(self, year_id: int) -> list[SchoolCalendarDetail]:
        curr_year = self.school_year_repo.get_by_id(year_id)
        if curr_year is None:
            raise NotFoundError(f"Год с id={year_id} не найден")
        existing = self.school_calendar_repo.get_by_year(year_id)
        if existing:
            raise ConflictError(f"Календарь для года {year_id} уже создан")

        days_data = []
        curr_day = curr_year.start_date
        while curr_day <= curr_year.end_date:
            if curr_day.weekday() >= 5:
                day_type = DayType.WEEKEND
            else:
                day_type = DayType.SCHOOL_DAY

            days_data.append({
                "year_id": year_id,
                "calendar_date": curr_day,
                "day_type": day_type
            })
            curr_day += timedelta(days=1)

        self.school_calendar_repo.create_calendar(days_data)
        created = self.school_calendar_repo.get_by_year(year_id)
        result = []
        for day in created:
            result.append(SchoolCalendarDetail.model_validate(day))
        return result

    def get_by_year(self, year_id: int) -> list[SchoolCalendarDetail]:
        curr_calendar = self.school_calendar_repo.get_by_year(year_id)
        result = []
        for day in curr_calendar:
            result.append(SchoolCalendarDetail.model_validate(day))
        return result

    def get_by_date(self, year_id: int, target_date: date) -> SchoolCalendarDetail | None:
        curr_date = self.school_calendar_repo.get_by_date(year_id, target_date)
        if curr_date is None:
            return None
        return SchoolCalendarDetail.model_validate(curr_date)

    def update_day(self, entry_id: int, data: SchoolCalendarUpdate) -> SchoolCalendarDetail:
        updated = self.school_calendar_repo.update_day(
            calendar_id=entry_id,
            day_type=data.day_type,
        )
        if updated is None:
            raise NotFoundError(f"Запись календаря с id={entry_id} не найдена")
        return SchoolCalendarDetail.model_validate(updated)

    def delete_calendar(self, year_id: int) -> None:
        year = self.school_year_repo.get_by_id(year_id)
        if year is None:
            raise NotFoundError(f"Год с id={year_id} не найден")

        existing = self.school_calendar_repo.get_by_year(year_id)
        if not existing:
            raise ConflictError(f"Календарь для года {year_id} ещё не создан")

        self.school_calendar_repo.delete_by_year(year_id)