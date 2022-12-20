from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .priority_tracks import *
from .recommender import *
from .data_retrieval_algorithms import *
from .search_results import *
from django.core.serializers import serialize

class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = 'artist-list'

class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    name = 'track-list'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

class TrackDetail(generics.RetrieveUpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    name = 'song-detail'

class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    name = 'genre-list'

class PlaylistList(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    name = 'playlist-list'

class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    name = 'album-list'

class TrackResults(generics.ListAPIView):
        queryset = Track.objects.all().order_by('-popularity')
        serializer_class = ResultSerializer
        name = 'track-list'
        filter_backends = [filters.SearchFilter, DjangoFilterBackend]
        search_fields = ['name', 'artists__name']


class GetUserPlaylist(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        data = playlist_list_view(username)
        return Response(data=data)

class AddUserPlaylist(APIView):

    def post(self, request, *args, **kwargs):
        uri = request.data.get('uri')
        exists = Playlist.objects.filter(uri=uri).exists()
        if exists:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)

        load_single_playlist(uri)
        add_priority_playlist(uri)
        print('done')
        return Response(status=status.HTTP_201_CREATED)

class AddSearchResults(APIView):

    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        track_search(query)
        return Response(status=status.HTTP_201_CREATED)

class RecommendSongs(APIView):

    def post(self, request, *args, **kwargs):
        uri = request.data.get('uri')
        dataset = request.data.get('dataset')
        measure = request.data.get('measure')

        results = search_popular(uri, output_playlist=dataset, SIMILARITY_MEASURE=measure)
        tracks = Track.objects.filter(uri__in=results)
        serializer = ResultSerializer(tracks, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
        
