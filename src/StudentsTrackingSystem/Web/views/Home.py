from django.shortcuts import render, redirect
from Bll.Services.User import UserService
from Dal.database import SessionLocal

def home(request):
    user_id = request.session.get("user_id")
    if user_id is None:
        return redirect("login")
    with SessionLocal() as session:
        service = UserService(session)
        user = service.get_by_id(user_id)
    
    return render(request, "Home.html", {"user": user})