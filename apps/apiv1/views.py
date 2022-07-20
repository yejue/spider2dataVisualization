from apps.visualization.models import CityModel, HouseInfoModel, DistrictModel, EstateModel

from libs.views import SimpleViewSet
# Create your views here.


class CitySimpleViewSet(SimpleViewSet):
    """城市表视图集合"""
    operation_fields = ["id", "city_name", "subdomain"]
    model = CityModel
    base_name = "city_list"


class DistrictSimpleViewSet(SimpleViewSet):
    """辖区表视图集合"""
    operation_fields = ["id", "city_id", "district_name", "lon", "lat", "avg_price", "house_code", "parent_id"]
    model = DistrictModel
    base_name = "district_list"


class EstateSimpleViewSet(SimpleViewSet):
    """小区表视图集合"""
    operation_fields = ["id", "district_id", "estate_name", "lon", "lat", "avg_price", "house_code"]
    model = EstateModel
    base_name = "estate_list"


class HouseInfoSimpleViewSet(SimpleViewSet):
    """房子表视图集合"""
    operation_fields = [
        "id", "title", "house_code", "location", "house_type", "house_area", "total_price", "unit_price", "estate_id",
    ]
    model = HouseInfoModel
    base_name = "house_list"
