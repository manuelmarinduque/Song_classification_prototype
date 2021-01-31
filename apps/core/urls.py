from django.urls import path

from .views import LoginView, HomeView, GeneratePlaylistView, CreateSelectedPlaylist

# Create your ulrs here.

app_name = 'core'

urlpatterns = [
    path('', LoginView.as_view(), name='login_page'),
    path('home/', HomeView.as_view(), name='home_page'),
    path('playlist/', GeneratePlaylistView.as_view(), name='playlist_page'),
    # TODO Quizás pueda funcionar el framework 'messages' de Django, el cual envía mensajes de la vista al template. Leer la documentación.
    # TODO Quizás se pueda emplear un FBV como se hace en la app 'collector'.
    # TODO Quizás se pueda emplear una CBV distinta, en la cual se sobreescriba el método get_success_url(), como se hace en el proyecto web_playground.
    path('playlist/<confirmation>', GeneratePlaylistView.as_view(), name='playlist_confirmation_page'),
    path('create_playlist/<playlist_value>/', CreateSelectedPlaylist.as_view(), name='create_playlist_page'),
]
