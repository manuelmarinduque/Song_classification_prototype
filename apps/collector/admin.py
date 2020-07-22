from django.contrib import admin

from . import models

# Register your models here.


class ArtistAdmin(admin.ModelAdmin):
    ordering = ('name', 'popularity', 'followers')
    search_fields = ('name', 'id')


class AlbumAdmin(admin.ModelAdmin):
    ordering = ('name', 'popularity', 'artist')
    search_fields = ('name', 'artist', 'id')


class SongAdmin(admin.ModelAdmin):
    ordering = ('name', 'album', 'popularity', 'energy', 'tempo', 'valence')
    search_fields = ('name', 'album', 'id')

admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Song, SongAdmin)
