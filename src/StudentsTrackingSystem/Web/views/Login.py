from django.shortcuts import render, redirect
from django.contrib import messages
from Dal.database import SessionLocal
from Bll.Services.User import UserService

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or not password:
            messages.error(request, "Введите логин или пароль!")
            return render(request, "Login.html")
        with SessionLocal() as session:
            service = UserService(session)
            user = service.authenticate(username, password)
        if user is None:
            messages.error(request, "Неверный логин или пароль")
            return render(request, "Login.html")

        request.session["user_id"] = user.id
        return redirect("home")
    return render(request, "Login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")