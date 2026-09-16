from enum import Enum

class DayType(Enum):
    SCHOOL_DAY = "school_day"
    WEEKEND = "weekend"
    HOLIDAY = "holiday" # гос праздники
    VACATION = "vacation" # каникулы
    OTHER = "other"

class GradeType(Enum):
    CLASSWORK = "class_work"
    HOMEWORK = "home_work"
    TEST = "test"