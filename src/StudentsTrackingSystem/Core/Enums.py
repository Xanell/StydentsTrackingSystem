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
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

    ALL = (STUDENT, TEACHER, ADMIN)


class RoleLabel:
    STUDENT = "Ученик"
    TEACHER = "Учитель"
    ADMIN = "Администратор"
