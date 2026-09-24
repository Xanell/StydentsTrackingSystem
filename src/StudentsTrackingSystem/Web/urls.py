from django.urls import path
from Web.views.Login import login_view, logout_view
from Web.views.Home import home
from Web.views.Users import users_view
from Web.views.SchoolYears import school_years_list, school_year_create, school_year_edit, school_year_make_current
from Web.views.SchoolClasses import school_classes_list, school_class_create, school_class_edit, classes_root

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
    path("users/", users_view, name="users"),
    path("school-years/", school_years_list, name="school_years"),
    path("school-years/create/", school_year_create, name="school_year_create"),
    path("school-years/<int:year_id>/edit/", school_year_edit, name="school_year_edit"),
    path("school-years/<int:year_id>/make-current/", school_year_make_current, name="school_year_make_current"),
    path("school-years/<int:year_id>/classes/", school_classes_list, name="school_classes"),
    path("school-years/<int:year_id>/classes/create/", school_class_create, name="school_class_create"),
    path("school-years/<int:year_id>/classes/<int:class_id>/edit/", school_class_edit, name="school_class_edit"),
    path("classes/", classes_root, name="classes_root")
]
print("users_view =", users_view)
print("type =", type(users_view))