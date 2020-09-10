from django.db import models

# Create your models here.

class SongsCatalogue(models.Model):
    name = models.CharField(max_length=300)
    identifier = models.CharField(max_length=50, unique=True)
    popularity = models.SmallIntegerField()
    duration_ms = models.SmallIntegerField()
    energy = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    danceability = models.FloatField()
    key = models.SmallIntegerField()
    loudness = models.FloatField()
    mode = models.SmallIntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    time_signature = models.SmallIntegerField()
    album_identifier = models.CharField(max_length=50)
    album_name = models.CharField(max_length=300)
    album_popularity = models.SmallIntegerField()
    artist_identifier = models.CharField(max_length=50)
    artist_name = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogo de canciones"

    def __str__(self):
        return self.name