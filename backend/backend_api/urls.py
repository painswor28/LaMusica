from django.conf.urls import url
from django.urls import path, include
from .views import (
    SongListApiView,
)

urlpatterns = [
    path('api', SongListApiView.as_view()),
]