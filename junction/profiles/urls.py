from django.conf.urls import url

from . import views

app_name = "junction.profiles"

urlpatterns = [
    url(r"^$", views.dashboard, name="dashboard"),
    url(r"^edit/$", views.profile, name="profile"),
]
