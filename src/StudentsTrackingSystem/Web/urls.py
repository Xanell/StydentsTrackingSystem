from django.urls import path
from Web.views.test import test

urlpatterns = [
    path("", test, name="test"),
]