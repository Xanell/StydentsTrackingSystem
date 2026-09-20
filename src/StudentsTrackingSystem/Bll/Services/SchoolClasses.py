from sqlalchemy.orm import Session
from Bll.Schemas.SchoolClasses import SchoolClassCreate, SchoolClassShort, SchoolClassUpdate
from Dal.Repositories.SchoolClasses import SchoolClassesRepository
from Dal.Repositories.SchoolYear import SchoolYearRepository

class SchoolClassService:
    def __init__(self, session: Session):
        self.school_class_repo = SchoolClassesRepository(session)
        self.school_year_repo = SchoolYearRepository(session)

    def create_class(self, data: SchoolClassCreate) -> SchoolClassShort:
        year = self.school_year_repo.get_by_id(data.school_year_id)
        if year is None:
            raise ValueError("Ошибка!")

        existing = self.school_class_repo.get_by_number_letter_year(data.number, data.letter, data.school_year_id)
        if existing is not None:
            raise ValueError("Ошибка такой класс уже существует!")

        new_class = self.school_class_repo.create_class(
            number=data.number,
            letter=data.letter,
            school_year_id=data.school_year_id
        )
        return SchoolClassShort.model_validate(new_class)

    def get_by_id(self, school_class_id: int) -> SchoolClassShort:
        school_class = self.school_class_repo.get_class_by_id(school_class_id)
        if school_class is None:
            raise ValueError("Ошибка такого класса нету!")

        return SchoolClassShort.model_validate(school_class)

    def get_all_classes(self, year_id: int) -> list[SchoolClassShort]:
        year = self.school_year_repo.get_by_id(year_id)
        if year is None:
            raise ValueError(f"Год с id={year_id} не найден")

        school_classes = self.school_class_repo.get_classes_by_year(year_id)
        result = []
        for school_class in school_classes:
            result.append(SchoolClassShort.model_validate(school_class))
        return result

    def update_class(self, class_id: int, data: SchoolClassUpdate) -> SchoolClassShort:
        school_class = self.school_class_repo.get_class_by_id(class_id)
        if school_class is None:
            raise ValueError("Ошибка такого класса нету!")

        new_number = data.number or school_class.number
        new_letter = data.letter or school_class.letter

        if new_number != school_class.number or new_letter != school_class.letter:
            existing = self.school_class_repo.get_by_number_letter_year(
                new_number, new_letter, school_class.school_year_id
            )
            if existing is not None:
                raise ValueError(f"Класс {new_number}{new_letter} уже существует в этом году")

        updated = self.school_class_repo.update_class(
            class_id,
            number=new_number,
            letter=new_letter
        )
        return SchoolClassShort.model_validate(updated)
