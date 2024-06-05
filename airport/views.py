from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from airport.models import (
    AirplaneType,
    Airplane,
    Crew,
    Country,
    City,
    Airport,
    Route,
    Flight,
    Order
)
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
    FlightDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
    AirplaneImageSerializer,
    AirportImageSerializer
)


def params_to_ints(qs):
    """Converts a list of string IDs to a list of integers"""
    return [int(str_id) for str_id in qs.split(",")]


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

    def get_queryset(self):
        """Retrieve the airplanes with airplane_type filter"""
        airplane_types = self.request.query_params.get("airplane_types")
        queryset = self.queryset
        if airplane_types:
            airplane_types_ids = params_to_ints(airplane_types)
            queryset = queryset.filter(
                airplane_type__id__in=airplane_types_ids
            )
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer

        if self.action == "upload_image":
            return AirplaneImageSerializer

        return AirplaneSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific airplane"""
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "airplane_types",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by airplane_type id (ex. ?airplane_types=2,5)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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

    def get_queryset(self):
        """Retrieve the airports with closest_big_city filter"""
        closest_big_city = self.request.query_params.get("closest_big_city")
        queryset = self.queryset
        if closest_big_city:
            queryset = queryset.filter(
                closest_big_city__name__icontains=closest_big_city
            )
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        if self.action == "retrieve":
            return AirportDetailSerializer

        if self.action == "upload_image":
            return AirportImageSerializer

        return AirportSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific airport"""
        airport = self.get_object()
        serializer = self.get_serializer(airport, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "closest_big_city",
                type=OpenApiTypes.STR,
                description="Filter by closest_big_city (ex. ?closest_big_city=Paris)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Route.objects.select_related("source", "destination")

    def get_queryset(self):
        """Retrieve the routes with filters"""
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        queryset = self.queryset
        if source:
            queryset = queryset.filter(
                source__closest_big_city__name__icontains=source
            )
        if destination:
            queryset = queryset.filter(
                destination__closest_big_city__name__icontains=destination
            )
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by source (ex. ?source=Paris)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filter by destination id (ex. ?destination=Kyiv)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
        .annotate(
            tickets_available=(
                    F("airplane__rows")
                    * F("airplane__seats_in_row")
                    - Count("tickets")
            )
        )
    )

    def get_queryset(self):
        """Retrieve the flights with filters"""
        routes = self.request.query_params.get("routes")
        airplanes = self.request.query_params.get("airplanes")
        crews = self.request.query_params.get("crews")
        queryset = self.queryset
        if routes:
            routes_ids = params_to_ints(routes)
            queryset = queryset.filter(route__id__in=routes_ids)
        if airplanes:
            airplanes_ids = params_to_ints(airplanes)
            queryset = queryset.filter(airplane__id__in=airplanes_ids)
        if crews:
            crews_ids = params_to_ints(crews)
            queryset = queryset.filter(crew__id__in=crews_ids)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "routes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by route id (ex. ?route=2,5)",
            ),
            OpenApiParameter(
                "airplanes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by airplane id (ex. ?airplane=2,5)",
            ),
            OpenApiParameter(
                "crews",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by crew id (ex. ?crew=2,5)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route",
        "tickets__flight__airplane",
        "tickets__flight__crew"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
