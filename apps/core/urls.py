from django.urls import path

from .views import LoginView, HomeView, GeneratePlaylistView, CreateSelectedPlaylist

# Create your ulrs here.

app_name = 'core'

urlpatterns = [
    path('', LoginView.as_view(), name='login_page'),
    path('home/', HomeView.as_view(), name='home_page'),
    path('playlist/', GeneratePlaylistView.as_view(), name='playlist_page'),
    path('create_playlist/<playlist_value>/', CreateSelectedPlaylist.as_view(), name='create_playlist_page'),
]
