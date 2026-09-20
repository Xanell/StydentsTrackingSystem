from sqlalchemy.orm import Session
from Bll.Schemas.Schedule import ScheduleCreate, ScheduleDetail, ScheduleUpdate
from Dal.Repositories.Schedule import ScheduleRepository
from Dal.Repositories.SchoolClasses import SchoolClassesRepository
from Dal.Repositories.Subjects import SubjectsRepository
from Dal.Repositories.LessonsPeriods import LessonsPeriodsRepository
from Dal.Repositories.User import UserRepository

class SheduleService:
    def __init__(self, session: Session):
        self.shedule_repo = ScheduleRepository(session)
        self.school_class_repo = SchoolClassesRepository(session)
        self.subject_repo = SubjectsRepository(session)
        self.period_repo = LessonsPeriodsRepository(session)
        self.user_repo = UserRepository(session)

    def create_shedule(self, data: ScheduleCreate) -> ScheduleDetail:

        if self.school_class_repo.get_class_by_id(data.class_id) is None:
            raise ValueError("Ошибка: класс не найден!")

        if self.subject_repo.get_by_id(data.subject_id) is None:
            raise ValueError("Ошибка: предмет не найден!")

        teacher = self.user_repo.get_by_id(data.teacher_id)

        if teacher is None:
            raise ValueError("Ошибка: учитель не найден!")

        if self.period_repo.get_by_id(data.period_id) is None:
            raise ValueError("Ошибка: период не найден!")

        room = data.room.strip()

        if not room:
            raise ValueError("Ошибка: кабинет не может быть пустым!")

        new_shedule = self.shedule_repo.create_schedule(
            class_id=data.class_id,
            subject_id=data.subject_id,
            teacher_id=data.teacher_id,
            period_id=data.period_id,
            day_of_week=data.day_of_week
            room=room
        )

        return ScheduleDetail.model_validate(new_shedule)

    def get_by_id(self, shedule_id: int) -> ScheduleDetail:

        shedule = self.shedule_repo.get_schedule_by_id(shedule_id)

        if shedule is None:
            raise ValueError("Ошибка: расписание не найдено!")

    def get_all_shedule(self) -> list[ScheduleDetail]:

        all_shedule = self.shedule_repo.get_all_schedule()
        result = []

        for shedule in all_shedule:
                result.append(ScheduleDetail.model_validate(shedule))
        return result  

    def get_by_class(self, class_id: int) -> list[ScheduleDetail]:

        class_shedule = self.school_class_repo.get_class_by_id(class_id)
        result =[]

        if self.school_class_repo.get_class_by_id(class_id) is None:
            raise ValueError("Ошибка: класс не найден!")

        for cls in class_shedule:
            result.append(ScheduleDetail.model_validate(cls))
        return result

    def get_by_teacher(self, teacher_id: int) -> list[ScheduleDetail]:

        teacher_shedule = self.user_repo.get_by_id(teacher_id)
        result = []

        if self.user_repo.get_by_id(teacher_id) is None:
            raise ValueError("Ошибка: учитель не найден!")

        for teacher in teacher_shedule:
            result.append(ScheduleDetail.model_validate(teacher))
        return result

    def update_shedule(self, shedule_id: int, data: ScheduleUpdate) -> ScheduleDetail:

        if self.shedule_repo.get_schedule_by_id(shedule_id) is None:
            raise ValueError("Ошибка: запись не найдена!")

        new_subject_id = data.subject_id
        if data.subject is None:
            raise ValueError("Ошибка: не может быть пустым!")
        
        new_teacher_id = data.teacher_id
        if data.teacher is None:
            raise ValueError("Ошибка: не может быть пустым!")

        new_room = data.room
        if data.room is None:
            raise ValueError("Ошибка: не может быть пустым!")
        
        new_day_of_week = data.day_of_week
        if data.day_of_week is None:
            raise ValueError("Ошибка: не может быть пустым!")

        if self.subject_repo.get_by_id(data.subject_id) is None:
            raise ValueError("Ошибка: предмет не найден!")

        if self.user_repo.get_by_id(data.teacher_id) is None:
            raise ValueError("Ошибка: учитель не найден!")

        update = self.shedule_repo.update_schedule(
            subject_id=new_subject_id,
            teacher_id=new_teacher_id,
            room=new_room
            day_of_week=new_day_of_week
        )
        return ScheduleDetail.model_validate(update)


        
            


