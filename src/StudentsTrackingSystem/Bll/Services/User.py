from sqlalchemy.orm import Session
from Bll.Schemas.User import UserCreate, UserCreatedResponse, UserUpdate, UserDetail, UserShort, UserPasswordResetResponse
from Dal.Repositories.User import UserRepository
from Dal.Repositories.UserRole import UserRoleRepository
from Dal.Repositories.SchoolClasses import SchoolClassesRepository
from Core.Enums import RoleName
from Core.Exceptions import NotFoundError, BusinessValidationError

class UserService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)
        self.user_role_repo = UserRoleRepository(session)
        self.school_class_repo = SchoolClassesRepository(session)

    def _generate_username(self, first_name: str, middle_name: str, last_name: str) -> str:
        base = f"{last_name}{first_name[0].upper()}{middle_name[0].upper()}"
        new_username = base
        if self.user_repo.get_by_username(new_username) is not None:
            counter = 2
            while self.user_repo.get_by_username(f"{base}{counter}") is not None:
                counter += 1
            new_username = f"{base}{counter}"
        return new_username
    
    def create_user(self, data: UserCreate) -> UserCreatedResponse:
        role = self.user_role_repo.get_by_id(data.role_id)
        if role is None:
            raise NotFoundError(f"Роль с id={data.role_id} не найдена")

        if data.class_id is not None:
            if self.school_class_repo.get_class_by_id(data.class_id) is None:
                raise NotFoundError(f"Класс с id={data.class_id} не найден")
            if role.name != RoleName.STUDENT:
                raise BusinessValidationError("Только ученик может быть привязан к классу")

        username = self._generate_username(data.first_name, data.middle_name, data.last_name)
        # добавить генерацию пароля + хеш
        password = "password"

        new_user = self.user_repo.create_user(
            username=username,
            password=password,
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            role_id=data.role_id,
            class_id=data.class_id
        )
        return UserCreatedResponse(id=new_user.id, username=new_user.username,password=password)

    def get_by_id(self, user_id: int) -> UserDetail:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"Пользователь с id={user_id} не найден")
        return UserDetail.model_validate(user)

    def get_all(self) -> list[UserDetail]:
        users = self.user_repo.get_all()
        result = []
        for user in users:
            result.append(UserDetail.model_validate(user))
        return result

    def get_by_role(self, role_name: str) -> list[UserShort]:
        role = self.user_role_repo.get_by_name(role_name)
        if role is None:
            raise NotFoundError(f"Роль '{role_name}' не найдена")

        users = self.user_repo.get_by_role(role_name)
        result = []
        for user in users:
            result.append(UserShort.model_validate(user))
        return result

    def reset_password(self, user_id: int) -> UserPasswordResetResponse:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"Пользователь с id={user_id} не найден")

        # заменить на генерацию пароля
        new_password = "new_password"
        self.user_repo.update_user(user_id, password=new_password)

        return UserPasswordResetResponse(
            id=user.id,
            username=user.username,
            password=new_password,
        )

    def update_user(self, user_id: int, data: UserUpdate) -> UserDetail:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"Пользователь с id={user_id} не найден")

        new_first_name = data.first_name or user.first_name
        new_middle_name = data.middle_name or user.middle_name
        new_last_name = data.last_name or user.last_name
        new_role_id = data.role_id or user.role_id
        new_class_id = data.class_id or user.class_id

        role = self.user_role_repo.get_by_id(new_role_id)
        if role is None:
            raise NotFoundError(f"Роль с id={new_role_id} не найдена")

        if new_class_id is not None:
            # Класс указан — проверить, что роль = ученик
            if role.name != RoleName.STUDENT:
                raise BusinessValidationError(
                    "Только ученик может быть привязан к классу"
                )
            # Проверить, что класс существует
            if self.school_class_repo.get_class_by_id(new_class_id) is None:
                raise NotFoundError(f"Класс с id={new_class_id} не найден")

        update = self.user_repo.update_user(
            user_id,
            first_name=new_first_name,
            middle_name=new_middle_name,
            last_name=new_last_name,
            role_id=new_role_id,
            class_id=new_class_id,
        )
        return UserDetail.model_validate(update)

    def authenticate(self, username: str, password: str) -> UserDetail | None:
        user = self.user_repo.get_by_username(username)
        if user is None:
            return None

        if user.password != password:
            return None

        return UserDetail.model_validate(user)
