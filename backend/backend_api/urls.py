from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('songs/', SongList.as_view(), name='song-list'),
    path('artists/', ArtistList.as_view(), name='artist-list'),
    path('songs/<int:pk>/', SongDetail.as_view(), name='song-detail'),
    path('tracks', TrackList.as_view(), name='track-list'),
    path('tracks/<str:pk>/', TrackDetail.as_view(), name='track-detail')
]