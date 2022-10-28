from django.db import models

# Create your models here.

class Songs(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length = 255)
    songKey = models.CharField(max_length = 255)
    tempo = models.IntegerField()

    def __str__(self):
        return self.SongID
