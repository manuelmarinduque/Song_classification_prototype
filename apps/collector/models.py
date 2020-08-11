from django.db import models

# Create your models here.


class Artist(models.Model):
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=300)
    popularity = models.SmallIntegerField()
    followers = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Artista"
        verbose_name_plural = "Artistas"

    def __str__(self):
        return self.name


class Album(models.Model):
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=300)
    popularity = models.SmallIntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    year = models.CharField(max_length=6)

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=300)
    identifier = models.CharField(max_length=50, unique=True)
    popularity = models.SmallIntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
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
    sentiment = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "Cancion"
        verbose_name_plural = "Canciones"

    def __str__(self):
        return self.name
        