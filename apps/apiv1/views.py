from apps.visualization.models import CityModel, HouseInfoModel
from libs.views import SimpleViewSet
# Create your views here.


class CityViewSet(SimpleViewSet):
    """
    城市视图集合
     - uri: /api/city_list/
     - uri: /api/city_list/:pk/
    """
    model = CityModel
    operation_fields = ["id", "city_name", "subdomain"]
    base_name = "city_list"


class HouseInfoViewSet(SimpleViewSet):
    """
    房子信息视图集合
     - uri: /api/house_list/
     - uri: /api/house_list/:pk/
    """
    model = HouseInfoModel
    operation_fields = [
        "id", "title", "house_code", "estate", "location", "house_type", "house_area", "total_price", "unit_price"
    ]
    base_name = "house_list"
