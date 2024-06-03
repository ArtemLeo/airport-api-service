from rest_framework import viewsets, mixins

from airport.models import AirplaneType, Airplane
from airport.serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer
)


class AirplaneTypeViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
