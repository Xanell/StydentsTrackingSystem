from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from Dal.database import get_session
from Bll.Services.SchoolClasses import SchoolClassService
from Bll.Services.SchoolYear import SchoolYearService
from Bll.Schemas.SchoolClasses import SchoolClassCreate, SchoolClassUpdate


def _require_login(request):
    if not request.session.get("user_id"):
        return redirect("login")
    return None

def classes_root(request):
    r = _require_login(request)
    if r:
        return r

    with get_session() as db:
        year_service = SchoolYearService(db)
        current = year_service.get_current()

    if current is None:
        messages.error(request, "Текущий учебный год не установлен")
        return redirect("school_years")

    return redirect("school_classes", year_id=current.id)

def school_classes_list(request, year_id: int):
    redirect_response = _require_login(request)
    if redirect_response:
        return redirect_response

    with get_session() as db:
        year_service = SchoolYearService(db)
        class_service = SchoolClassService(db)

        try:
            year = year_service.get_by_id(year_id)
        except ValueError:
            raise Http404("Учебный год не найден")

        classes = class_service.get_all_classes(year_id)

    return render(request, "school_classes/list.html", {
        "year": year,
        "year_id": year_id,
        "classes": classes,
    })


def school_class_create(request, year_id: int):
    redirect_response = _require_login(request)
    if redirect_response:
        return redirect_response

    with get_session() as db:
        year_service = SchoolYearService(db)
        class_service = SchoolClassService(db)

        try:
            year = year_service.get_by_id(year_id)
        except ValueError:
            raise Http404("Учебный год не найден")

        if request.method == "POST":
            try:
                data = SchoolClassCreate(
                    number=int(request.POST["number"]),
                    letter=request.POST["letter"],
                    school_year_id=year_id,
                )
                new_class = class_service.create_class(data)
                messages.success(
                    request,
                    f"Класс {new_class.number}{new_class.letter} создан"
                )
                return redirect("school_classes", year_id=year_id)
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Ошибка: {e}")

        return render(request, "school_classes/form.html", {
            "action": "create",
            "year": year,
            "year_id": year_id,
            "school_class": None,
        })


def school_class_edit(request, year_id: int, class_id: int):
    redirect_response = _require_login(request)
    if redirect_response:
        return redirect_response

    with get_session() as db:
        class_service = SchoolClassService(db)

        try:
            school_class = class_service.get_by_id(class_id)
        except ValueError:
            raise Http404("Класс не найден")

        if request.method == "POST":
            try:
                data = SchoolClassUpdate(
                    number=int(request.POST["number"]) if request.POST.get("number") else None,
                    letter=request.POST.get("letter") or None,
                )
                updated = class_service.update_class(class_id, data)
                messages.success(
                    request,
                    f"Класс {updated.number}{updated.letter} обновлён"
                )
                return redirect("school_classes", year_id=school_class.school_year_id
                                if hasattr(school_class, "school_year_id") else 0)
            except ValueError as e:
                messages.error(request, str(e))

        return render(request, "school_classes/form.html", {
            "action": "edit",
            "year": None,
            "year_id": year_id,
            "school_class": school_class,
        })