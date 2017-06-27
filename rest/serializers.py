from rest_framework import serializers

class FactsSerializer(serializers.Serializer):
    json = serializers.JSONField