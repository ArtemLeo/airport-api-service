from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Flight
from airport.serializers import FlightListSerializer
from airport.tests.sample_data import sample_flight, sample_route, sample_airplane

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        sample_flight()
        sample_flight()

        res = self.client.get(FLIGHT_URL)

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for index, serializer_object in enumerate(serializer.data):
            for key in serializer_object:
                self.assertEqual(serializer_object[key], res.data[index][key])

    def test_filter_flights_by_routes(self):
        route1 = sample_route(distance=1111)
        route2 = sample_route(distance=2222)
        route3 = sample_route(distance=3333)

        flight1 = sample_flight(route=route1)
        flight2 = sample_flight(route=route2)
        flight3 = sample_flight(route=route3)

        res = self.client.get(
            FLIGHT_URL, {"routes": f"{route1.id}, {route2.id}"}
        )

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_flights_by_airplanes(self):
        airplane1 = sample_airplane(name="Airplane 1")
        airplane2 = sample_airplane(name="Airplane 2")
        airplane3 = sample_airplane(name="Airplane 3")

        flight1 = sample_flight(airplane=airplane1)
        flight2 = sample_flight(airplane=airplane2)
        flight3 = sample_flight(airplane=airplane3)

        res = self.client.get(
            FLIGHT_URL, {"airplanes": f"{airplane1.id}, {airplane2.id}"}
        )

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
