from django.db import models

# Create your models here.

class Songs(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length = 255)
    songKey = models.CharField(max_length = 255)
    tempo = models.IntegerField()

    def __str__(self):
        return self.id

class Track(models.Model):
    uri = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=50)
    id = models.CharField(max_length=25)
    danceability = models.FloatField()
    energy = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumental = models.FloatField()
    liveness = models.FloatField()
    valance = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.FloatField()
    time_signature = models.FloatField()
    camelot_key = models.CharField(max_length=2)
    popularity = models.FloatField()
    explicit = models.BooleanField()
    preview_url = models.CharField(max_length=250)
    spotify_url = models.CharField(max_length=250)

    def __str__(self):
        return self.uri