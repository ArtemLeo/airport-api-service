from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport
from airport.serializers import AirportListSerializer, AirportDetailSerializer
from airport.tests.sample_data import sample_airport, sample_city

AIRPORT_URL = reverse("airport:airport-list")


def detail_url(airport_id):
    return reverse("airport:airport-detail", args=[airport_id])


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

    def test_create_airport_forbidden(self):
        city = sample_city()

        payload = {
            "name": "Forbidden Airport",
            "closest_big_city": city.pk
        }

        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        city = sample_city()

        payload = {
            "name": "Test Airport",
            "closest_big_city": city.pk
        }

        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        airport = Airport.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], airport.name)
        self.assertEqual(city, airport.closest_big_city)
