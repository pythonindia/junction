from django.urls import re_path

from . import views

app_name = "junction.profiles"

urlpatterns = [
    re_path(r"^$", views.dashboard, name="dashboard"),
    #you can also use instead of re_path , path and include like 
    #path(url_type, view_function, name)
    re_path(r"^edit/$", views.profile, name="profile"),
]
