from enum import Enum

class DayType(str, Enum):
    SCHOOL_DAY = "school_day"
    WEEKEND = "weekend"
    HOLIDAY = "holiday" # гос праздники
    VACATION = "vacation" # каникулы
    OTHER = "other"

class GradeType(str, Enum):
    CLASSWORK = "class_work"
    HOMEWORK = "home_work"
    TEST = "test"

class RoleName:
    USER = "user"
    TEACHER = "teacher"
    ADMIN = "admin"

    ALL = (USER, TEACHER, ADMIN)


class RoleLabel:
    USER = "Ученик"
    TEACHER = "Учитель"
    ADMIN = "Администратор"
