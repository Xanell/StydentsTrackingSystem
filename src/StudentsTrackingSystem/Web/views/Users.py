from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from Bll.Services.UserRole import UserRoleService
from Bll.Services.User import UserService
from Bll.Services.SchoolClasses import SchoolClassService
from Bll.Services.SchoolYear import SchoolYearService
from Bll.Schemas.User import UserCreate, UserUpdate
from Dal.database import SessionLocal
from Core.Exceptions import BllError, NotFoundError
from Web.Decorators import login_required, role_required
from Core.Enums import RoleName

@login_required
@role_required(RoleName.ADMIN)
def users_list(request):
    with SessionLocal() as session:
        user_service = UserService(session)
        users_list = user_service.get_all()

    return render(request, "users/List.html", {"users": users_list})

@login_required
@role_required(RoleName.ADMIN)
def user_create(request):
    with SessionLocal() as session:
        user_service = UserService(session)
        class_service = SchoolClassService(session)
        role_service = UserRoleService(session)
        year_service = SchoolYearService(session)
        current_year = year_service.get_current()

        if current_year is None:
            messages.error(request, "Текущий год не установлен!")
            return redirect("school_years")

        roles = role_service.get_all()
        classes = class_service.get_all_classes(current_year.id)

        if request.method == "POST":
            try:
                data = UserCreate(
                    first_name=request.POST.get("first_name", "").strip(),
                    middle_name=request.POST.get("middle_name", "").strip(),
                    last_name=request.POST.get("last_name", "").strip(),
                    role_id=request.POST.get("role_id") or None,
                    class_id=request.POST.get("class_id") or None
                )
                created = user_service.create_user(data)
                request.session["created_user"] = {
                    "id": created.id,
                    "username": created.username,
                    "password": created.password,
                }
                return redirect("user_created")
            except BllError as e:
                messages.error(request, str(e))
        return render(request, "users/Form.html", {
            "action": "create",
            "roles": roles,
            "classes": classes,
            "user": None,
        })

@login_required
@role_required(RoleName.ADMIN)
def user_created(request):
    data = request.session.pop("created_user", None)
    if data is None:
        return redirect("users")
    return render(request, "users/Created.html", data)

@login_required
@role_required(RoleName.ADMIN)
def user_edit(request, user_id: int):
    with SessionLocal() as session:
        user_service = UserService(session)
        role_service = UserRoleService(session)
        class_service = SchoolClassService(session)
        year_service = SchoolYearService(session)

        current_year = year_service.get_current()
        if current_year is None:
            messages.error(request, "Текущий год не установлен")
            return redirect("school_years")
        
        try:
            user = user_service.get_by_id(user_id)
        except NotFoundError:
            raise Http404("Пользователь не найден")

        roles = role_service.get_all()
        classes = class_service.get_all_classes(current_year.id)

        if request.method == "POST":
            try:
                data = UserUpdate(
                    first_name=request.POST.get("first_name", "").strip() or None,
                    middle_name=request.POST.get("middle_name", "").strip() or None,
                    last_name=request.POST.get("last_name", "").strip() or None,
                    role_id=request.POST.get("role_id") or None,
                    class_id=request.POST.get("class_id") or None
                )
                update = user_service.update_user(user_id, data)
                messages.success(request, f"Пользователь {update.username} обновлён")
                return redirect("users")
            except BllError as e:
                messages.error(request, str(e))

        return render(request, "users/Form.html", {
            "action": "edit",
            "user": user,
            "roles": roles,
            "classes": classes,
        })