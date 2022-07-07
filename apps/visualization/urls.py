from django.urls import path
from .views import LianJiaCitySpiderView, LianJiaSecondHandSpiderView, LianJiaDistrictSpiderView

app_name = "visualization"

urlpatterns = [
    path("add_city/", LianJiaCitySpiderView.as_view(), name="add_city"),
    path("add_district/", LianJiaDistrictSpiderView.as_view(), name="add_district"),
    path("add_data/", LianJiaSecondHandSpiderView.as_view(), name="add_data"),
]
