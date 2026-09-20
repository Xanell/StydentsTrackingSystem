from sqlalchemy.orm import Session
from Bll.Schemas.Schedule import ScheduleCreate, ScheduleDetail, ScheduleUpdate
from Dal.Repositories.Schedule import ScheduleRepository
from Dal.Repositories.SchoolClasses import SchoolClassesRepository
from Dal.Repositories.Subjects import SubjectsRepository
from Dal.Repositories.LessonsPeriods import LessonsPeriodsRepository
from Dal.Repositories.User import UserRepository
from Core.Enums import RoleName

class ScheduleService:
    def __init__(self, session: Session):
        self.schedule_repo = ScheduleRepository(session)
        self.school_class_repo = SchoolClassesRepository(session)
        self.subject_repo = SubjectsRepository(session)
        self.period_repo = LessonsPeriodsRepository(session)
        self.user_repo = UserRepository(session)

    def create_schedule(self, data: ScheduleCreate) -> ScheduleDetail:

        if self.school_class_repo.get_class_by_id(data.class_id) is None:
            raise ValueError("Ошибка: класс не найден!")

        if self.subject_repo.get_by_id(data.subject_id) is None:
            raise ValueError("Ошибка: предмет не найден!")

        teacher = self.user_repo.get_by_id(data.teacher_id)
        if teacher is None:
            raise ValueError(f"Пользователь с id={data.teacher_id} не найден")
        if teacher.role.name != RoleName.TEACHER:
            raise ValueError(f"Пользователь с id={data.teacher_id} не является учителем")

        if self.period_repo.get_by_id(data.period_id) is None:
            raise ValueError("Ошибка: период не найден!")

        existing = self.schedule_repo.get_by_class_day_period(data.class_id, data.day_of_week, data.period_id)
        if existing is not None:
            raise ValueError(f"У класса уже есть урок в день {data.day_of_week}, период {data.period_id}")

        room = data.room.strip()
        if not room:
            raise ValueError("Ошибка: кабинет не может быть пустым!")

        new_schedule = self.schedule_repo.create_schedule(
            class_id=data.class_id,
            subject_id=data.subject_id,
            teacher_id=data.teacher_id,
            period_id=data.period_id,
            day_of_week=data.day_of_week,
            room=room
        )

        return ScheduleDetail.model_validate(new_schedule)

    def get_by_id(self, schedule_id: int) -> ScheduleDetail:

        schedule = self.schedule_repo.get_schedule_by_id(schedule_id)

        if schedule is None:
            raise ValueError("Ошибка: расписание не найдено!")
        return ScheduleDetail.model_validate(schedule)

    def get_all_schedule(self) -> list[ScheduleDetail]:

        all_schedule = self.schedule_repo.get_all_schedule()
        result = []

        for schedule in all_schedule:
                result.append(ScheduleDetail.model_validate(schedule))
        return result 

    def get_by_class(self, class_id: int) -> list[ScheduleDetail]:

        if self.school_class_repo.get_class_by_id(class_id) is None:
            raise ValueError(f"Класс с id={class_id} не найден")

        schedules = self.schedule_repo.get_schedule_by_class(class_id)
        result = []
        for schedule in schedules:
            result.append(ScheduleDetail.model_validate(schedule))
        return result

    def get_by_teacher(self, teacher_id: int) -> list[ScheduleDetail]:

        teacher = self.user_repo.get_by_id(teacher_id)
        if teacher is None:
            raise ValueError(f"Пользователь с id={teacher_id} не найден")
        if teacher.role.name != RoleName.TEACHER:
            raise ValueError(f"Пользователь с id={teacher_id} не является учителем")

        schedules = self.schedule_repo.get_schedule_by_teacher(teacher_id)
        result = []
        for schedule in schedules:
            result.append(ScheduleDetail.model_validate(schedule))
        return result

    def update_schedule(self, schedule_id: int, data: ScheduleUpdate) -> ScheduleDetail:
        
        schedule = self.schedule_repo.get_schedule_by_id(schedule_id)
        if schedule is None:
            raise ValueError(f"Расписание с id={schedule_id} не найдено")

        new_subject_id = data.subject_id or schedule.subject_id
        new_teacher_id = data.teacher_id or schedule.teacher_id
        new_room = data.room if data.room is not None else schedule.room
        new_day_of_week = (
            data.day_of_week if data.day_of_week is not None else schedule.day_of_week
        )

        if new_subject_id != schedule.subject_id:
            if self.subject_repo.get_by_id(new_subject_id) is None:
                raise ValueError(f"Предмет с id={new_subject_id} не найден")

        if new_teacher_id != schedule.teacher_id:
            teacher = self.user_repo.get_by_id(new_teacher_id)
            if teacher is None:
                raise ValueError(f"Пользователь с id={new_teacher_id} не найден")
            if teacher.role.name != RoleName.TEACHER:
                raise ValueError(f"Пользователь с id={new_teacher_id} не является учителем")

        if new_day_of_week != schedule.day_of_week:
            existing = self.schedule_repo.get_by_class_day_period(
                schedule.class_id,
                new_day_of_week,
                schedule.period_id,
            )
            if existing is not None and existing.id != schedule_id:
                raise ValueError(
                    f"В этот день (period {schedule.period_id}) у класса уже есть урок"
                )

        update = self.schedule_repo.update_schedule(
            schedule_id,
            subject_id=new_subject_id,
            teacher_id=new_teacher_id,
            room=new_room,
            day_of_week=new_day_of_week,
        )
        return ScheduleDetail.model_validate(update)