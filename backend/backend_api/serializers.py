from rest_framework import serializers
from .models import Songs

class songSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("id", "artist", "songKey", "tempo")