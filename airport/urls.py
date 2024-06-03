from rest_framework import routers

from airport.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet
)

router = routers.DefaultRouter()

router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = router.urls

app_name = "airport"
