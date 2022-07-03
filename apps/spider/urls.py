from django.urls import path
from .views import LianJiaCitySpiderView, LianJiaSecondHandSpiderView

app_name = "spider"

urlpatterns = [
    path("add_city/", LianJiaCitySpiderView.as_view(), name="city_spider"),
    path("add_data/", LianJiaSecondHandSpiderView.as_view(), name="second_hand_spider"),
]
