from rest_framework import serializers
from .models import *

class songSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("id", "artist", "songKey", "tempo")

class trackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("uri", "name", "id", "danceability", "energy", "loudness", "speechiness", "acousticness", "instrumental", "liveness", "valance", "tempo", "duration_ms", "time_signature", "camelot_key", "popularity", "explicit", "preview_url", "spotify_url")
