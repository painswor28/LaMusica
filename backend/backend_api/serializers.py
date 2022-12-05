from rest_framework import serializers
from .models import *

class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    #album = serializers.PrimaryKeyRelatedField(read_only=True)
    #artists = serializers.PrimaryKeyRelatedField(many=True, queryset=Artist.objects.all()) 

    class Meta:
        model = Track
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

    
class PlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'
