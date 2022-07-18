from django.contrib import admin
from .models import CityModel, HouseInfoModel, DistrictModel, EstateModel

from libs.admin import BaseAdmin
# Register your models here.


class CityAdmin(BaseAdmin):
    """城市管理类"""
    list_display = ["id", "city_name", "subdomain"]
    search_fields = ["city_name", "subdomain"]


class DistrictAdmin(BaseAdmin):
    """辖区管理类"""
    list_display = ["id", "city", "district_name", "parent", "lon", "lat"]
    search_fields = ["district_name", "city__city_name"]


class EstateAdmin(BaseAdmin):
    """小区管理类"""
    list_display = ["id", "estate_name", "district", "house_code", "lon", "lat"]
    search_fields = ["estate_name", "house_code", "district__district_name"]


class HouseInfoAdmin(BaseAdmin):
    """房子信息管理类"""
    list_display = ["id", "title", "estate", "house_type", "house_area", "total_price", "house_code"]
    search_fields = [
        "title", "house_type", "house_code", "estate__estate_name", "estate__district__parent__district_name"
    ]


admin.site.register(CityModel, CityAdmin)
admin.site.register(HouseInfoModel, HouseInfoAdmin)
admin.site.register(DistrictModel, DistrictAdmin)
admin.site.register(EstateModel, EstateAdmin)
