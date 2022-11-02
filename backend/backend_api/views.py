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

class SongList(generics.ListCreateAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongSerializer
    name = 'song-list'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ['artists__name']

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongSerializer
    name = 'song-detail'

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
