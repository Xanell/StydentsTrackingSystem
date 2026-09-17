from Dal.repositories.User import UserRepository
from Dal.repositories.UserRole import UserRoleRepository
from Core.Enums import RoleName

def role_seed(session):
    role_repo = UserRoleRepository(session)

    for name in RoleName.ALL:
        existing = role_repo.get_by_name(name)
        if existing is None:
            role_repo.create_role(name)

def admin_seed(session, username="Admin", password="admin"):
    user_repo = UserRepository(session)
    role_repo = UserRoleRepository(session)

    if user_repo.get_by_username(username) is not None:
        return

    admin_role = role_repo.get_by_name(RoleName.ADMIN)
    if admin_role is None:
        raise RuntimeError("Роль 'admin' не найдена. Сначала запусти seed_roles().")

    admin = user_repo.create_user(
        username=username,
        password=password,
        first_name="Admin",
        last_name="Admin",
        middle_name="Admin",
        role_id=admin_role.id,
        class_id=None,
    )