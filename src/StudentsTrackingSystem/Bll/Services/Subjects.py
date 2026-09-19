from sqlalchemy.orm import Session
from Bll.Schemas.Subject import SubjectCreate, SubjectDetail, SubjectShort, SubjectUpdate
<<<<<<< HEAD
from Dal.repositories.Subjects import SubjectsRepository
=======
from Dal.Repositories.Subjects import SubjectsRepository
>>>>>>> origin/master

class SubjectService:
    def __init__(self, session: Session):
        self.subject_repo = SubjectsRepository(session)

<<<<<<< HEAD
    def create_subject(self, subject: SubjectCreate) -> SubjectDetail:

        if not subject.name:
            raise ValueError("Ошибка: не может быть пустым!")

        if self.subject_repo.get_by_name(subject.name) is not None:
            raise ValueError("Ошибка: предмет уже существует!")

        new_subject = self.subject_repo.create_subject(name=subject.name, description=subject.description)

        return SubjectCreate.model_validate(new_subject)

    def get_by_id(self, subject_id: int) -> SubjectDetail:

        subject = self.subject_repo.get_by_id(subject_id)

        if subject is None:
            raise ValueError("Ошибка: Предмет не найден!")

        return SubjectDetail.model_validate(subject)

    def get_by_name(self, name: str) -> SubjectDetail:

        subject = self.subject_repo.get_by_name(name)

        if subject is None:
            raise ValueError("Ошибка: Предмет не найден!")
        
        return SubjectDetail.model_validate(subject)

    def get_all(self) -> list[SubjectShort]:

        subjects = self.subject_repo.get_all()

        return [SubjectShort.model_validate(subj) for subj in subjects]

    def update_subject(self, subject_id: int, subject: SubjectUpdate) -> SubjectDetail:

        subj = self.subject_repo.get_by_id(subject_id)

        if subj is None:
            raise ValueError("Ошибка: Предмет не найден!")

        if subject.name is not None:
            new_name = subject.name

            if not new_name:
                raise ValueError("Ошибка: Не может быть пустым!")

        if subject.description is not None:
            new_description = subject.description

        update = self.subject_repo.update_subject(name=new_name, description=new_description)

        return SubjectDetail.model_validate(update)

    def delete_subject(self, subject_id: int) -> None:
        
        if not self.subject_repo.delete_subject(subject_id):
            raise ValueError(f"Ошибка: Предмет не найден")



=======
    def create_subject(self, data: SubjectCreate) -> SubjectDetail:
        if self.subject_repo.get_by_name(data.name) is not None:
            raise ValueError("Ошибка!!")

        new_subject = self.subject_repo.create_subject(name=data.name, description=data.description)
        return SubjectDetail.model_validate(new_subject)

    def get_by_id(self, subject_id: int) -> SubjectDetail:
        curr_subject = self.subject_repo.get_by_id(subject_id)
        if curr_subject is None:
            raise ValueError("Ошибка!!")

        return SubjectDetail.model_validate(curr_subject)

    def get_all(self) -> list[SubjectShort]:
        subjects = self.subject_repo.get_all()
        result = []
        for subject in subjects:
            result.append(SubjectShort.model_validate(subject))
        return result

    def update_subject(self, subject_id: int, data: SubjectUpdate) -> SubjectDetail:
        curr_subject = self.subject_repo.get_by_id(subject_id)
        if curr_subject is None:
            raise ValueError("Ошибка!!")

        if data.name is not None and data.name != curr_subject.name:
            existing = self.subject_repo.get_by_name(data.name)
            if existing is not None:
                raise ValueError("Такое название предмета уже есть!")

        updated = self.subject_repo.update_subject(
            subject_id=subject_id,
            name=data.name,
            description=data.description
        )
        return SubjectDetail.model_validate(updated)

    def delete_subject(self, subject_id: int) -> None:
        curr_subject = self.subject_repo.get_by_id(subject_id)
        if curr_subject is None:
            raise ValueError("Ошибка!")

        if curr_subject.schedule: 
            raise ValueError("Ошибка предмет есть в расписание!")

        self.subject_repo.delete_subject(subject_id)
>>>>>>> origin/master
