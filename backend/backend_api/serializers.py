from rest_framework import serializers
from .models import *

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Songs
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):

    songs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
