from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..DTOs.SchoolCalendar import SchoolCalendar
from Core.Enums import DayType

class SchoolCalendarRepository:     # Репозиторий для работы с календарём учебного года

    def __init__(self, session: Session):
        self.db = session

    def create_calendar(self, year_id: int, calendar_date: date, quarter: int, day_type: DayType) -> SchoolCalendar:

        """Создать запись в календаре"""

        calendar = SchoolCalendar(year_id = year_id, calendar_date = calendar_date, quarter = quarter, day_type = day_type)

        self.db.add(calendar)
        self.db.commit()
        self.db.refresh(calendar)

        return calendar

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

        stmt = (select(SchoolCalendar)).where(SchoolCalendar.year_id == year_id, SchoolCalendar.day_type == day_type).order_by(SchoolCalendar.calendar_date)

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

    def update_by_date(self, year_id: int, target_date: date, day_type: DayType) -> SchoolCalendar | None:

        """Обновить тип дня по дате"""

        calendar = self.get_by_date(year_id, target_date)
        if calendar is None:
            return None
        
        calendar.day_type = day_type
        self.db.commit()
        self.db.refresh(calendar)

        return calendar

    def mark_as_school_day(self, year_id: int, target_date: date) -> bool:

        """Отметить день как учебный"""

        return self.update_by_date(year_id, target_date, DayType.SCHOOL_DAY) is not None

    def mark_as_holiday(self, year_id: int, target_date: date) -> bool:

        """Отметить день как праздничный"""

        return self.update_by_date(year_id, target_date, DayType.HOLIDAY) is not None

    def mark_as_vacation(self, year_id: int, target_date: date) -> bool:

        """Отметить день как каникулы"""

        return self.update_by_date(year_id, target_date, DayType.VACATION) is not None

    def delete_record(self, calendar_id: int) -> bool:

        """Удалить запись"""

        calendar = self.db.get(SchoolCalendar, calendar_id)

        self.db.delete(calendar)
        self.db.commit()

        return True

    def delete_by_date(self, year_id: int, target_date: date) -> bool:
        calendar = self.get_by_date(year_id, target_date)
        if calendar is None:
            return False
        self.db.delete(calendar)
        self.db.commit()
        return True
