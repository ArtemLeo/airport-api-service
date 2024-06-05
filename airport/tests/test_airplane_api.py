from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

AIRPLANE_URL = reverse("airport:airplane-list")


def detail_url(airplane_id):
    return reverse("airport:airplane-detail", args=[airplane_id])


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
