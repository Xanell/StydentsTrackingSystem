from sqlalchemy.orm import Session
from Bll.Schemas.Lessons import LessonDetail, LessonCreate, LessonUpdate
from Dal.Repositories.Lessons import LessonsRepository
from Dal.Repositories.Schedule import ScheduleRepository
from datetime import date
from Core.Exceptions import NotFoundError, ConflictError, BusinessValidationError

class LessonService:
    def __init__(self, session: Session):
        self.lesson_repo = LessonsRepository(session)
        self.schedule_repo = ScheduleRepository(session)

    def get_by_id(self, lesson_id: int) -> LessonDetail:
        lesson = self.lesson_repo.get_by_id(lesson_id)
        if lesson is None:
            raise NotFoundError("Ошибка урок не найден")
        return LessonDetail.model_validate(lesson)

    def get_all_lessons(self) -> list[LessonDetail]:
        all_lessons = self.lesson_repo.get_all()
        result = []
        for lesson in all_lessons:
            result.append(LessonDetail.model_validate(lesson))
        return result

    def get_by_schedule(self, schedule_id: int) -> list[LessonDetail]:
        lessons = self.lesson_repo.get_by_schedule(schedule_id)
        result = []
        for lesson in lessons:
            result.append(LessonDetail.model_validate(lesson))
        return result

    def get_by_date(self, lesson_date: date) -> list[LessonDetail]:
        lessons = self.lesson_repo.get_by_date(lesson_date)
        result = []
        for lesson in lessons:
            result.append(LessonDetail.model_validate(lesson))
        return result

    def create_lesson(self, data: LessonCreate) -> LessonDetail:
        if self.schedule_repo.get_schedule_by_id(data.schedule_id) is None:
            raise NotFoundError(f"Расписание #{data.schedule_id} не найдено")

        if data.homework_due_date is not None and data.homework_due_date < data.lesson_date:
            raise BusinessValidationError("Дедлайн домашки не может быть раньше даты урока")

        existing = self.lesson_repo.get_by_schedule_and_date(
            data.schedule_id, data.lesson_date
        )
        if existing is not None:
            raise ConflictError(
                f"Урок на {data.lesson_date} по этому расписанию уже существует"
            )

        new_lesson = self.lesson_repo.create_lesson(
            lesson_date=data.lesson_date,
            topic=data.topic,
            homework_description=data.homework_description,
            homework_due_date=data.homework_due_date,
            files=data.files,
            schedule_id=data.schedule_id
        )
        return LessonDetail.model_validate(new_lesson)

    def update_lesson(self, lesson_id: int, data: LessonUpdate) -> LessonDetail:
        lesson = self.lesson_repo.get_by_id(lesson_id)
        if lesson is None:
            raise NotFoundError(f"Урок #{lesson_id} не найден")

        new_topic = data.topic if data.topic is not None else lesson.topic
        new_homework_description = (
            data.homework_description if data.homework_description is not None
            else lesson.homework_description
        )
        new_homework_due_date = (
            data.homework_due_date if data.homework_due_date is not None
            else lesson.homework_due_date
        )
        new_files = data.files if data.files is not None else lesson.files

        if new_homework_due_date is not None and new_homework_due_date < lesson.lesson_date:
            raise BusinessValidationError("Дедлайн домашки не может быть раньше даты урока")

        update = self.lesson_repo.update_lesson(
            lesson_id,
            topic=new_topic,
            homework_description=new_homework_description,
            homework_due_date=new_homework_due_date,
            files=new_files,
        )
        return LessonDetail.model_validate(update)