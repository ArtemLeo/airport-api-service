from rest_framework import routers
from airport.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    CountryViewSet,
    CityViewSet
)

router = routers.DefaultRouter()
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crews", CrewViewSet)
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)

urlpatterns = router.urls

app_name = "airport"
