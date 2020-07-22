import spotipy

from apps.collector.models import Artist, Album, Song


class Collector():

    def __init__(self, artist_uri):
        self.artist_uri = artist_uri
        self.connection = self.__getAccessSpotify()

    def __getAccessSpotify(self):
        credentials = spotipy.SpotifyClientCredentials(
            '55c64375790e42f298941e9bdd0dbbc0', '47744189d3844da0a5f57aada4747d79')
        token = credentials.get_access_token()
        connection = spotipy.Spotify(auth=token)
        return connection

    def getArtistInformation(self, dict_artist_info):
        artist_info = {'identifier': dict_artist_info.get('id'),
                       'name': dict_artist_info.get('name'),
                       'popularity': dict_artist_info.get('popularity'),
                       'followers': dict_artist_info.get('followers').get('total')}
        artist_object = Artist(**artist_info)
        self.__addDatabase(artist_object)
        return artist_object

    def getArtistAlbums(self, artist_object):
        for album_object in self.__getArtistAlbumsInformation(artist_object):
            self.__addDatabase(album_object)
            self.__getAlbumSongs(album_object)

    def __getArtistAlbumsInformation(self, artist_object):
        artist_albums_info = self.connection.artist_albums(
            self.artist_uri, 'album', 'CO')
        artist_albums = artist_albums_info.get('items')[::-1]
        for album in artist_albums:
            album_name = album.get('name').lower()
            if self.__validationFindNotWords(album_name, 'album'):
                continue
            else:
                album_id = album.get('id')
                album_popularity = self.__getPopularity(album_id, 'album')
                if album_popularity >= 47:
                    album_info = {'name': album_name,
                                  'identifier': album_id,
                                  'artist': artist_object,
                                  'popularity': album_popularity}
                    album_object = Album(**album_info)
                    yield album_object
                else:
                    continue

    def __getPopularity(self, identifier, type_of):
        if type_of == 'song':
            dict_info = self.connection.track(identifier)
        else:
            dict_info = self.connection.album(identifier)
        popularity = dict_info.get('popularity')
        return popularity

    def __validationFindNotWords(self, element_name, type_of):
        var = False
        if type_of == 'song':
            not_words = ('version', 'live', 'en vivo', 'mix', 'remix', 'mtv', '(vivo)',
                         'instrumental', 'versión')
        else:
            not_words = ('gira', 'tour', 'live', 'mtv', 'commentary', 'en vivo', 'mix',
                         'plug', 'unplugged', 'concierto', 'concert')
        for word in not_words:
            if element_name.find(word) != -1:
                var = True
        return var

    def __getAlbumSongs(self, album_object):
        for song_element in self.__getAlbumSongsInformation(album_object):
            self.__addDatabase(song_element)
            # print(song_element.album.artist.name)

    def __getAlbumSongsInformation(self, album_object):
        album_songs_info = self.connection.album_tracks(
            album_object.identifier, market='CO')
        album_songs = album_songs_info.get('items')
        for song in album_songs:
            song_name = song.get('name').lower()
            if self.__validationFindNotWords(song_name, 'song'):
                continue
            else:
                song_id = song.get('id')
                song_popularity = self.__getPopularity(song_id, 'song')
                song_info = self.__getAudioFeatures(
                    song_id, song_name, song_popularity, album_object)
                song_object = Song(**song_info)
                yield song_object

    def __validationAddDatabase(self, object_element):
        if isinstance(object_element, Song):
            in_database = Song.objects.filter(
                identifier=object_element.identifier).exists()
            in_database = self.__validationSongNameArtist(object_element)
        elif isinstance(object_element, Album):
            in_database = Album.objects.filter(
                identifier=object_element.identifier).exists()
        else:
            in_database = Artist.objects.filter(
                identifier=object_element.identifier).exists()
        return in_database

    def __addDatabase(self, object_element):
        if self.__validationAddDatabase(object_element):
            pass
        else:
            object_element.save()

    def __validationSongNameArtist(self, song_object):
        in_database = Song.objects.filter(
            name=song_object.name, album__artist__identifier=self.artist_uri).exists()
        return in_database

    def __getAudioFeatures(self, song_id, song_name, song_popularity, album_object):
        dict_song_description = self.connection.audio_features(song_id)[0]
        song_audio_features = self.__getSongAtributes(dict_song_description)
        song_audio_features['identifier'] = song_id
        song_audio_features['name'] = song_name
        song_audio_features['popularity'] = song_popularity
        song_audio_features['album'] = album_object
        return song_audio_features

    def __getSongAtributes(self, dict_song_description):
        atributes_not_included = (
            'type', 'uri', 'track_href', 'analysis_url', 'id')
        song_atributes = {}
        for key, value in dict_song_description.items():
            if key not in atributes_not_included:
                song_atributes[key] = value
        return song_atributes
