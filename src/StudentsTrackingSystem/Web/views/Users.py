from django.shortcuts import render, redirect
from Bll.Services.User import UserService
from Dal.database import SessionLocal
from Web.Decorators import login_required

@login_required
def users_view(request):
    with SessionLocal() as session:
        service = UserService(session)
        users_list = service.get_all()

    return render(request, "Users.html", {"users": users_list})