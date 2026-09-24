from sqlalchemy.orm import Session
from Bll.Schemas.Subject import SubjectCreate, SubjectDetail, SubjectShort, SubjectUpdate
from Dal.Repositories.Subjects import SubjectsRepository
from Core.Exceptions import NotFoundError, ConflictError

class SubjectService:
    def __init__(self, session: Session):
        self.subject_repo = SubjectsRepository(session)

    def create_subject(self, data: SubjectCreate) -> SubjectDetail:
        if self.subject_repo.get_by_name(data.name) is not None:
            raise ConflictError(f"Предмет '{data.name}' уже существует")

        new_subject = self.subject_repo.create_subject(name=data.name, description=data.description)
        return SubjectDetail.model_validate(new_subject)

    def get_by_id(self, subject_id: int) -> SubjectDetail:
        curr_subject = self.subject_repo.get_by_id(subject_id)
        if curr_subject is None:
            raise NotFoundError(f"Предмет #{subject_id} не найден")

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
            raise NotFoundError(f"Предмет #{subject_id} не найден")

        if data.name is not None and data.name != curr_subject.name:
            existing = self.subject_repo.get_by_name(data.name)
            if existing is not None:
                raise ConflictError(f"Предмет '{data.name}' уже существует")

        updated = self.subject_repo.update_subject(
            subject_id=subject_id,
            name=data.name,
            description=data.description
        )
        return SubjectDetail.model_validate(updated)
