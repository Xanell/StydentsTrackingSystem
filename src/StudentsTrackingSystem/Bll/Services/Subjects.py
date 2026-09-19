from sqlalchemy.orm import Session
from Bll.Schemas.Subject import SubjectCreate, SubjectDetail, SubjectShort, SubjectUpdate
from Dal.repositories.Subjects import SubjectsRepository

class SubjectService:
    def __init__(self, session: Session):
        self.subject_repo = SubjectsRepository(session)

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



