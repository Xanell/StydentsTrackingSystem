from django.shortcuts import render, redirect
from Bll.Services.User import UserService
from Dal.database import SessionLocal

def users_view(request):
    user_id = request.session.get("user_id")
    if user_id is None:
        return redirect("login")

    with SessionLocal() as session:
        service = UserService(session)
        users_list = service.get_all()

    return render(request, "Users.html", {"users": users_list})