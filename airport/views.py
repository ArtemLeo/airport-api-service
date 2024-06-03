from rest_framework import viewsets, mixins

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer


class AirplaneTypeViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
