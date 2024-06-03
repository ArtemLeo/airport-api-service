from rest_framework import viewsets, mixins

from airport.models import AirplaneType, Airplane, Crew, Country, City, Airport, Route, Flight
from airport.serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneDetailSerializer,
    AirplaneListSerializer,
    CrewSerializer,
    CountrySerializer,
    CitySerializer,
    CityListSerializer,
    AirportSerializer,
    AirportDetailSerializer,
    AirportListSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightListSerializer,
    FlightSerializer,
    FlightDetailSerializer
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
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Airplane.objects.select_related("airplane_type")

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the airplanes with airplane_type filter"""
        airplane_types = self.request.query_params.get("airplane_type")
        queryset = self.queryset
        if airplane_types:
            airplane_types_ids = self._params_to_ints(airplane_types)
            queryset = queryset.filter(airplane_type__id__in=airplane_types_ids)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer


class CrewViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class CountryViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = City.objects.select_related("country")

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer

        return CitySerializer


class AirportViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Airport.objects.select_related("closest_big_city")

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the airports with closest_big_city filter"""
        closest_big_cities = self.request.query_params.get("closest_big_city")

        queryset = self.queryset

        if closest_big_cities:
            closest_big_cities_ids = self._params_to_ints(closest_big_cities)
            queryset = queryset.filter(closest_big_city__id__in=closest_big_cities_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer

        if self.action == "retrieve":
            return AirportDetailSerializer

        return AirportSerializer


class RouteViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Route.objects.select_related("source", "destination")

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the routes with filters"""
        sources = self.request.query_params.get("source")
        destinations = self.request.query_params.get("destination")

        queryset = self.queryset

        if sources:
            sources_ids = self._params_to_ints(sources)
            queryset = queryset.filter(source__id__in=sources_ids)

        if destinations:
            destinations_ids = self._params_to_ints(destinations)
            queryset = queryset.filter(destination__id__in=destinations_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer


class FlightViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = (
        Flight.objects
        .select_related("route", "airplane")
        .prefetch_related("crew")
    )

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the flights with filters"""
        routes = self.request.query_params.get("route")
        airplanes = self.request.query_params.get("airplane")
        crews = self.request.query_params.get("crew")

        queryset = self.queryset

        if routes:
            routes_ids = self._params_to_ints(routes)
            queryset = queryset.filter(route__id__in=routes_ids)

        if airplanes:
            airplanes_ids = self._params_to_ints(airplanes)
            queryset = queryset.filter(airplane__id__in=airplanes_ids)

        if crews:
            crews_ids = self._params_to_ints(crews)
            queryset = queryset.filter(crew__id__in=crews_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer
