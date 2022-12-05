# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Genre(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        db_table = 'backend_api_genre'

class Artist(models.Model):
    uri = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=150)
    link = models.CharField(max_length=150, null=True)
    image = models.CharField(max_length=150, null=True)
    popularity = models.FloatField()
    #genres = models.ManyToManyField(Genre)

    class Meta:
        db_table = 'backend_api_artist'


class Album(models.Model):
    uri = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    cover_image = models.CharField(max_length=150)
    release_date = models.DateField()
    #artists = models.ManyToManyField(Artist)

    class Meta:
        db_table = 'backend_api_album'

    def __str__(self):
        return self.name

class Track(models.Model):
    uri = models.CharField(primary_key=True, max_length=40)
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
    explicit = models.IntegerField()
    preview_url = models.CharField(max_length=250, blank=True, null=True)
    spotify_url = models.CharField(max_length=250)
    #album = models.ForeignKey(Album, models.DO_NOTHING)
    #artists = models.ManyToManyField(Artist)

    class Meta:
        db_table = 'backend_api_track'

class Playlist(models.Model):
    pid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    num_followers = models.IntegerField()
    #tracks = models.ManyToManyField(Track)

    class Meta:
        db_table = 'backend_api_playlist'