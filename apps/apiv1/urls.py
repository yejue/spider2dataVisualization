from apps.apiv1.views import EstateSimpleViewSet
from libs.routers import SimpleRouter

simple_router = SimpleRouter()
simple_router.register(EstateSimpleViewSet)

urlpatterns = [] + simple_router.get_urls()
