from rest_framework import serializers

from airport.models import AirplaneType


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"
