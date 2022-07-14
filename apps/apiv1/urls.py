from rest_framework import routers
from apps.apiv1.views import CityViewSet, HouseInfoViewSet, EstateViewSet, DistrictViewSet
from libs.routers import SimpleRouter

router = routers.DefaultRouter()
router.register(r'city_list', CityViewSet)
router.register(r'house_info_list', HouseInfoViewSet)
router.register(r'estate_list', EstateViewSet)
router.register(r'district_list', DistrictViewSet)

urlpatterns = router.urls


