from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('tracks/', TrackList.as_view(), name='track-list'),
    path('tracks/<str:pk>/', TrackDetail.as_view(), name='track-detail'),
    path('albums/', AlbumList.as_view(), name='album-list'),
    path('artists/', ArtistList.as_view(), name='artist-list'),
    path('genres/', GenreList.as_view(), name='genre-list'),
    path('playlists/', PlaylistList.as_view(), name='playlist-list'),
    path('results/', TrackResults.as_view(), name='track-results'),
]