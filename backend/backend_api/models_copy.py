from django.db import models

# Create your models here.

class Artist(models.Model):
    uri = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    image = models.CharField(max_length=150)
    popularity = models.FloatField()

class Track(models.Model):
    uri = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=150)
    danceability = models.FloatField()
    energy = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.FloatField()
    time_signature = models.FloatField()
    camelot_key = models.CharField(max_length=3)
    popularity = models.FloatField()
    explicit = models.BooleanField()
    preview_url = models.CharField(max_length=250, blank=True, null=True)
    spotify_url = models.CharField(max_length=250)
    album_id = 

    def __str__(self):
        return self.uri

class Album(models.Model):
    uri = models.CharField(max_length=40, primary_key=True)
    
