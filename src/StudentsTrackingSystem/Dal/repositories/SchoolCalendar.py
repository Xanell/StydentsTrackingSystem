from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from ..DTOs.SchoolCalendar import SchoolCalendar
from Core.Enums import DayType

class SchoolCalendarRepository:     # Репозиторий для работы с календарём учебного года

    def __init__(self, session: Session):
        self.db = session

    def create_calendar(self, days_data: list[dict]) -> None:

        """Создать запись в календаре"""

        objects = []
        for day in days_data:
            objects.append(SchoolCalendar(**day)) 
        self.db.add_all(objects)
        self.db.commit()

    def get_by_id(self, calendar_id: int) -> SchoolCalendar | None:

        """Получить по ID"""

        return self.db.get(SchoolCalendar, calendar_id)

    def get_by_date(self, year_id: int, target_date: date) -> SchoolCalendar | None:

        """Получить по конкретной дате"""

        stmt = select(SchoolCalendar).where(SchoolCalendar.year_id == year_id, SchoolCalendar.calendar_date == target_date)

        return self.db.scalars(stmt).one_or_none()

    def get_by_year(self, year_id: int) -> list[SchoolCalendar]:

        """Получить весь календарь учебного года"""

        stmt = (select(SchoolCalendar).where(SchoolCalendar.year_id == year_id).order_by(SchoolCalendar.calendar_date))

        return self.db.scalars(stmt).all()

    def get_by_day_type(self, year_id: int, day_type: DayType) -> list[SchoolCalendar]:

        """
        Получить все дни определённого типа:
        SCHOOL_DAY - учебный день
        HOLIDAY = праздник
        VACATION = каникулы
        """

        stmt = select(SchoolCalendar).where(SchoolCalendar.year_id == year_id, SchoolCalendar.day_type == day_type).order_by(SchoolCalendar.calendar_date)

        return self.db.scalars(stmt).all()

    def get_school_days(self, year_id: int) -> list[SchoolCalendar]:

        """Получить учебные дни"""

        return self.get_by_day_type(year_id, DayType.SCHOOL_DAY)

    def get_holidays(self, year_id: int) -> list[SchoolCalendar]:

        """Получить праздничные дни"""

        return self.get_by_day_type(year_id, DayType.HOLIDAY)

    def get_vacations(self, year_id: int) -> list[SchoolCalendar]:

        """Получить каникулы"""

        return self.get_by_day_type(year_id, DayType.VACATION)

    def update_day(self, calendar_id: int, day_type: DayType) -> SchoolCalendar | None:

        """Обновить тип дня"""

        entry = self.get_by_id(calendar_id)
        if entry is None:
            return None
        if day_type is not None:
            entry.day_type = day_type
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def delete_by_year(self, year_id: int) -> None:
        """Удалить все записи календаря для указанного года."""
        stmt = delete(SchoolCalendar).where(SchoolCalendar.year_id == year_id)
        self.db.execute(stmt)
        self.db.commit()