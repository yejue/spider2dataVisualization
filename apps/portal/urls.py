from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("distribution/", views.HousingPriceDistributionView.as_view(), name="distribution"),
    path("big-view/", views.BigViewView.as_view(), name="big_view"),
    path("video-list/", views.VideoListView.as_view(), name="video_list"),
]
