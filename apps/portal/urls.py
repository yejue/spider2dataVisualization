from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("distribution/", views.IndexView.as_view(), name="distribution"),
]
