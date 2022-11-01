from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('songs', SongListApiView.as_view()),
    path('songs/<int:id>/', SongDetailApiView.as_view()),
    path('tracks', trackListApiView.as_view()),
]