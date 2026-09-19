from sqlalchemy.orm import Session
from Bll.Schemas.Subject import SubjectCreate, SubjectDetail, SubjectShort, SubjectUpdate
from Dal.Repositories.Subjects import SubjectsRepository

class SubjectService:
    def __init__(self, session: Session):
        self.subject_repo = SubjectsRepository(session)

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