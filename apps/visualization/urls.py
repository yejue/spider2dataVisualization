from django.urls import path
from .views import LianJiaCitySpiderView, LianJiaSecondHandSpiderView

app_name = "visualization"

urlpatterns = [
    path("add_city/", LianJiaCitySpiderView.as_view(), name="add_city"),
    path("add_data/", LianJiaSecondHandSpiderView.as_view(), name="add_data"),
]
