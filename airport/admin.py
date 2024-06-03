from django.contrib import admin

from airport.models import (
    AirplaneType,
    Airplane
)


admin.site.register(AirplaneType)
admin.site.register(Airplane)
