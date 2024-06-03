from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}, {self.country}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE)
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)

    def __str__(self):
        return self.route


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {airplane_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self):
        return (
            f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"
        )
