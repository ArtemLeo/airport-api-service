from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import (
    Airplane,
    AirplaneType,
    Country,
    City,
    Airport,
    Route,
    Crew,
    Flight
)
from airport.serializers import AirportListSerializer, AirportDetailSerializer

AIRPLANE_URL = reverse("airport:airplane-list")
AIRPORT_URL = reverse("airport:airport-list")
FLIGHT_URL = reverse("airport:flight-list")


def detail_url(airport_id):
    return reverse("airport:airport-detail", args=[airport_id])


def sample_airplane(**params):
    airplane_type = AirplaneType.objects.create(
        name="Boeing 747"
    )

    defaults = {
        "name": "Skyliner X",
        "rows": 20,
        "seats_in_row": 4,
        "airplane_type": airplane_type
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


def sample_city(**params):
    country = Country.objects.create(name="France")

    defaults = {
        "name": "Paris",
        "country": country
    }
    defaults.update(params)

    return City.objects.create(**defaults)


def sample_airport(**params):
    city = sample_city()

    defaults = {
        "name": "Charles de Gaulle Airport",
        "closest_big_city": city
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_city(name="Source City")
    destination = sample_city(name="Destination City")

    defaults = {
        "source": source,
        "destination": destination,
        "distance": 3458
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    crew = Crew.objects.create(
        first_name="FirstName",
        last_name="LastName"
    )

    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2023-11-18 14:00:00",
        "arrival_time": "2023-11-18 19:00:00",
        "crew": crew
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        sample_airport()
        sample_airport()

        res = self.client.get(AIRPORT_URL)

        airports = Airport.objects.all()
        serializer = AirportListSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_airports_by_closest_big_city(self):
        city1 = sample_city(name="First City")
        city2 = sample_city(name="Second City")
        city3 = sample_city(name="Extra one")

        airport1 = sample_airport(name="Airport 1", closest_big_city=city1)
        airport2 = sample_airport(name="Airport 2", closest_big_city=city2)
        airport3 = sample_airport(name="Airport 3", closest_big_city=city3)

        res = self.client.get(
            AIRPORT_URL, {"closest_big_city": "City"}
        )

        serializer1 = AirportListSerializer(airport1)
        serializer2 = AirportListSerializer(airport2)
        serializer3 = AirportListSerializer(airport3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_airport_detail(self):
        airport = sample_airport()

        url = detail_url(airport.id)
        res = self.client.get(url)

        serializer = AirportDetailSerializer(airport)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
