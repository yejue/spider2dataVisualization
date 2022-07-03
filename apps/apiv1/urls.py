from .views import HouseInfoViewSet, CityViewSet
from libs.routers import SimpleRouter

app_name = "apiv1"

simple_router = SimpleRouter()

simple_router.register(HouseInfoViewSet)
simple_router.register(CityViewSet)

urlpatterns = [
]

urlpatterns += simple_router.get_urls()
