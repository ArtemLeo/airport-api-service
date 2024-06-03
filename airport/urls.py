from rest_framework import routers

from airport.views import AirplaneTypeViewSet

router = routers.DefaultRouter()

router.register("airplane_types", AirplaneTypeViewSet)

urlpatterns = router.urls

app_name = "airport"
