import spotipy
from statistics import quantiles
import pandas as pd

from apps.collector.models import Artist, Album, Song
from django.db.utils import IntegrityError


class Collector():

    def __init__(self, artist_id, token, user):
        self.artist_id = artist_id
        self.user = user
        self.connection = self.__getAccessSpotify(token)

    def __getAccessSpotify(self, token):
        connection = spotipy.Spotify(auth=token)
        return connection

    def getArtistObject(self, dict_artist_info):
        artist_info = {'identifier': self.artist_id,
                       'name': dict_artist_info.get('name'),
                       'popularity': dict_artist_info.get('popularity'),
                       'followers': dict_artist_info.get('followers').get('total')}
        artist_object = Artist(**artist_info)
        artist_object.save()
        return artist_object

    def getArtistAlbums(self, artist_object):
        for album_object in self.__getArtistAlbumsInformation(artist_object):
            self.__getAlbumSongs(album_object)

    def __getArtistAlbumsInformation(self, artist_object):
        artist_albums_info1 = self.connection.artist_albums(self.artist_id, 'album', 'CO', 50)
        artist_albums1 = artist_albums_info1.get('items')
        artist_albums_info2 = self.connection.artist_albums(self.artist_id, 'single', 'CO', 50)
        artist_albums2= artist_albums_info2.get('items')
        artist_albums = artist_albums1 + artist_albums2
        for album in artist_albums:
            album_name = album.get('name').lower()
            included_words = self.__validationIncludedWords(album_name, 'album')
            if not included_words:
                album_id = album.get('id')
                album_popularity = self.__getPopularity(album_id, 'album')
                if album_popularity >= 0:
                    album_year = album.get('release_date')[0:4]
                    album_info = {'name': album_name,
                                  'identifier': album_id,
                                  'artist': artist_object,
                                  'popularity': album_popularity,
                                  'year': album_year}
                    album_object = Album(**album_info)
                    try:
                        album_object.save()
                    except IntegrityError:
                        continue
                    else:
                        yield album_object

    def __getPopularity(self, identifier, type_of):
        if type_of == 'song':
            dict_info = self.connection.track(identifier)
        else:
            dict_info = self.connection.album(identifier)
        popularity = dict_info.get('popularity')
        return popularity

    def __validationIncludedWords(self, element_name, type_of):
        var = False
        if type_of == 'song':
            # Para los singles eliminar las palabras 'remix', 'version', 'versión'.
            avoid_words = ('- live', 'en vivo', '- vivo', 'en directo', '- directo')
        else:
            avoid_words = ('homenaje', 'live', 'mtv', 'commentary', 'en vivo', 'plug', 'unplugged', 'concierto', 'concert', 'track by track', 'primera fila', 'sinfónico', 'en directo')
        for word in avoid_words:
            if element_name.find(word) != -1:
                var = True
        return var

    def __getAlbumSongs(self, album_object):
        album_songs_info = self.connection.album_tracks(album_object.identifier, market='CO')
        album_songs = album_songs_info.get('items')
        for song in album_songs:
            song_name = song.get('name').lower()
            in_database = Song.objects.filter(name=song_name, album__artist__identifier=self.artist_id).exists()
            if not in_database:
                included_words = self.__validationIncludedWords(song_name, 'song')
                if not included_words:
                    song_id = song.get('id')
                    song_popularity = self.__getPopularity(song_id, 'song')
                    song_info = self.__getAudioFeatures(song_id, song_name, song_popularity, album_object)
                    song_object = Song(**song_info)
                    try:
                        song_object.save()
                    except IntegrityError:
                        continue

    def __getAudioFeatures(self, song_id, song_name, song_popularity, album_object):
        dict_song_description = self.connection.audio_features(song_id)[0]
        song_audio_features = self.__getSongAtributes(dict_song_description)
        song_audio_features['identifier'] = song_id
        song_audio_features['name'] = song_name
        song_audio_features['popularity'] = song_popularity
        song_audio_features['album'] = album_object
        return song_audio_features

    def __getSongAtributes(self, dict_song_description):
        atributes_not_included = ('type', 'uri', 'track_href', 'analysis_url', 'id')
        song_atributes = {}
        for key, value in dict_song_description.items():
            if key not in atributes_not_included:
                song_atributes[key] = value
        return song_atributes

    def readSavedTracks(self):
        n = 0
        tracks = []
        saved_tracks = []
        while not tracks:
            tracks = self.connection.current_user_saved_tracks(50, n)['items']
            saved_tracks.extend(tracks)
            n += 50
        ids_list = self.__generateIdsList(saved_tracks)
        audio_features_saved_tracks = self.__getAudioFeaturesSavedTracks(ids_list)
        return self.__createDataFrame(saved_tracks, audio_features_saved_tracks)

    def __generateIdsList(self, saved_tracks):
        ids_list = [track['track']['id'] for track in saved_tracks]
        return ids_list
    
    def __getAudioFeaturesSavedTracks(self, ids_list):
        start, end = 0, 99
        audio_features = []
        ids_list_aux = []
        while not ids_list_aux:
            ids_list_aux = ids_list[start:end]
            audio_features.extend(self.connection.audio_features(ids_list_aux))
            start = end
            end += 99
        return audio_features

    def __createDataFrame(self, saved_tracks, audio_features_saved_tracks):
        saved_tracks_df = pd.DataFrame(columns=('song_name', 'artist_name', 'track_id', 'id', 'acousticness',
        'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
        'tempo', 'valence'))
        for item, audio_feature in zip(saved_tracks, audio_features_saved_tracks):
            track = item['track']
            track_info = {'song_name': track['name'],
                          'artist_name': track['artists'][0]['name'], 
                          'track_id': track['id'],
                          'id': audio_feature['id'],
                          'acousticness': audio_feature['acousticness'],
                          'danceability': audio_feature['danceability'],
                          'duration_ms': audio_feature['duration_ms'],
                          'energy': audio_feature['energy'],
                          'instrumentalness': audio_feature['instrumentalness'],
                          'liveness': audio_feature['liveness'],
                          'loudness': audio_feature['loudness'],
                          'speechiness': audio_feature['speechiness'],
                          'tempo': audio_feature['tempo'],
                          'valence': audio_feature['valence']
                         }
            saved_tracks_df = saved_tracks_df.append(track_info, ignore_index=True)
        return saved_tracks_df

    def createPlaylist(self):
        self.connection.user_playlist_create(self.user, 'Nueva playlist desde el back', public=False)
