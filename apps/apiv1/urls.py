from apps.apiv1 import views
from libs.routers import SimpleRouter

simple_router = SimpleRouter()
simple_router.register(views.EstateSimpleViewSet)
simple_router.register(views.CitySimpleViewSet)
simple_router.register(views.DistrictSimpleViewSet)
simple_router.register(views.HouseInfoSimpleViewSet)

urlpatterns = [] + simple_router.get_urls()
