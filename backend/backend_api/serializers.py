from rest_framework import serializers
from .models import *

class ArtistSerializer(serializers.ModelSerializer):

    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())

    class Meta:
        model = Artist
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):

    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    artists = serializers.PrimaryKeyRelatedField(many=True, queryset=Artist.objects.all())

    class Meta:
        model = Track
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

    
class PlaylistSerializer(serializers.ModelSerializer):

    tracks = serializers.PrimaryKeyRelatedField(many=True, queryset=Track.objects.all())

    class Meta:
        model = Playlist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):

    artists = serializers.PrimaryKeyRelatedField(many=True, queryset=Artist.objects.all())

    class Meta:
        model = Album
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):

    album = AlbumSerializer(read_only=True)
    artists = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Track
        fields = '__all__'


class RecommendationSerializer(serializers.Serializer):

    fields = '__all__'

    def to_representation(self, instance):
        # Convert the data to a serializable format
        return {
        # Use the `fields` attribute of the serializer to get the list of fields to serialize
        field_name: getattr(instance, field_name) for field_name in self.fields
        }
