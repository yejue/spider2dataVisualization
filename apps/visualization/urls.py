from django.urls import path
from . import views

app_name = "visualization"

urlpatterns = [
    path("add_city/", views.LianJiaCitySpiderView.as_view(), name="add_city"),
    path("add_district/", views.LianJiaDistrictSpiderView.as_view(), name="add_district"),
    path("add_estate/", views.LianJiaEstateSpiderView.as_view(), name="add_estate"),
    path("add_data/", views.LianJiaSecondHandSpiderView.as_view(), name="add_data"),
    path("add_coordinate/", views.EstateAddCoordinateView.as_view(), name="add_coordinate"),
]
