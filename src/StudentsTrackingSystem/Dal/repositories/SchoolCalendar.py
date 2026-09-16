from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from ..DTOs.SchoolCalendar import SchoolCalendar
from Core.Enums import DayType

class SchoolCalendarRepository:     # Репозиторий для работы с календарём учебного года

    def __init__(self, db: Session):
        self.db = db

    def create_calendar(self, year_id: int, date: date, quarter: int, day_type: DayType) -> SchoolCalendar:

        """Создать запись в календаре"""

        calendar = SchoolCalendar(year_id = year_id, date = date, quarter = quarter, day_type = day_type)

        self.db.add(calendar)
        self.db.commit()
        self.db.refresh(calendar)

        return calendar

    def get_by_id(self, calendar_id: int) -> SchoolCalendar:

        """Получить по ID"""

        return self.db.get(SchoolCalendar, calendar_id)

    def get_by_date(self, year_id: int, target_date: date) -> SchoolCalendar:

        """Получить по конкретной дате"""

        stmt = select(SchoolCalendar).where(SchoolCalendar.year_id == year_id, SchoolCalendar.date == target_date)

        return self.db.scalars(stmt).first()

    def get_by_year(self, year_id: int) -> list[SchoolCalendar]:

        """Получить весь календарь учебного года"""

        stmt = (select(SchoolCalendar).where(SchoolCalendar.year_id == year_id).order_by(SchoolCalendar.date))

        return list(self.db.scalars(stmt).all())

    def get_by_day_type(self, year_id: int, day_type: DayType) -> list[SchoolCalendar]:

        """
        Получить все дни определённого типа:
        SCHOOL_DAY - учебный день
        HOLIDAY = праздник
        VACATION = каникулы
        """

        stmt = (select(SchoolCalendar)).where(SchoolCalendar.year_id == year_id, SchoolCalendar.day_type == day_type).order_by(SchoolCalendar.date)

        return list(self.db.scalars(stmt).all())

    def get_school_days(self, year_id: int) -> list[SchoolCalendar]:

        """Получить учебные дни"""

        return self.get_by_day_type(year_id, DayType.SCHOOL_DAY)

    def get_holidays(self, year_id: int) -> list[SchoolCalendar]:

        """Получить праздничные дни"""

        return self.get_by_day_type(year_id, DayType.HOLIDAY)

    def get_vacations(self, year_id: int) -> list[SchoolCalendar]:

        """Получить каникулы"""

        return self.get_by_day_type(year_id, DayType.VACATION)

    def update_by_date(self, year_id: int, target_date: date, day_type: DayType) -> SchoolCalendar:

        """Обновить тип дня по дате"""

        calendar = self.get_by_date(year_id, target_date)

        calendar.day_type = day_type

        self.db.commit()
        self.db.refresh(calendar)

        return calendar

    def mark_as_school_day(self, year_id: int, target_date: date) -> bool:

        """Отметить день как учебный"""

        result = self.update_by_date(year_id, target_date, DayType.SCHOOL_DAY)

        return result

    def mark_as_holiday(self, year_id: int, target_date: date) -> bool:

        """Отметить день как праздничный"""

        result = self.update_by_date(year_id, target_date, DayType.HOLIDAY)

        return result

    def mark_as_vacation(self, year_id: int, target_date: date) -> bool:

        """Отметить день как каникулы"""

        result = self.update_by_date(year_id, target_date, DayType.VACATION)

        return result

    def delete_record(self, calendar_id: int) -> bool:

        """Удалить запись"""

        calendar = self.db.get(SchoolCalendar, calendar_id)

        self.db.delete(calendar)
        self.db.commit()

        return True

    def delete_by_date(self, year_id: int, target_date: date) -> bool:

        """Удалить запись по дате"""

        stmt = delete(SchoolCalendar).where(SchoolCalendar.year_id == year_id, SchoolCalendar.date == target_date)

        self.db.delete(stmt)
        self.db.commit()

        return True
