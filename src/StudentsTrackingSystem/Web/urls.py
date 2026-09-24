from django.urls import path
from Web.views.Login import login_view, logout_view
from Web.views.Home import home
from Web.views.Users import users_view
from Web.views.SchoolYears import school_years_list, school_year_create, school_year_edit, school_year_make_current


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
    path("users/", users_view, name="users"),
    path("school-years/", school_years_list, name="school_years"),
    path("school-years/create/", school_year_create, name="school_year_create"),
    path("school-years/<int:year_id>/edit/", school_year_edit, name="school_year_edit"),
    path("school-years/<int:year_id>/make-current/", school_year_make_current, name="school_year_make_current")
]
