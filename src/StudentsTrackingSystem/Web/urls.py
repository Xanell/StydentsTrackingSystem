from django.urls import path
from Web.views.Login import login_view, logout_view
from Web.views.Home import home
from Web.views.Users import users_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
    path("users/", users_view, name="users")
]