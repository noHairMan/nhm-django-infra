from rest_framework import serializers

from porsche.core.restframework.serializer import PorscheSerializer


class HealthCheckResponseSerializer(PorscheSerializer):
    app = serializers.CharField()
    version = serializers.CharField()
    debug = serializers.BooleanField()
