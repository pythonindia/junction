from django.urls import re_path

from . import views

app_name = "junction.profiles"

urlpatterns = [
    re_path(r"^$", views.dashboard, name="dashboard"),
    re_path(r"^edit/$", views.profile, name="profile"),
]
