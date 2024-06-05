from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
