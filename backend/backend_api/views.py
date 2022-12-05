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


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    name = 'song-detail'

class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    name = 'genre-list'

class PlaylistList(generics.ListCreateAPIView):
    queryset = Playlist.objects.all().order_by('-num_followers').values()
    serializer_class = PlaylistSerializer
    name = 'playlist-list'

class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    name = 'album-list'


class TrackResults(generics.ListAPIView):
    queryset = Track.objects.all().order_by('-popularity')
    serializer_class = TrackSerializer
    name = 'track-list'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']


