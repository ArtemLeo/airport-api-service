from django.urls import reverse

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

AIRPLANE_URL = reverse("airport:airplane-list")
AIRPORT_URL = reverse("airport:airport-list")
FLIGHT_URL = reverse("airport:flight-list")


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
