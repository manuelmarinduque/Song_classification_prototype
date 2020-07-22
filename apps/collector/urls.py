from django.urls import path

from . import views

# Create yours urls here.

app_name = 'collector'

urlpatterns = [
    path('search_artist', views.searchArtist, name='search_artist_page'),
    path('search_artist/<str:artist_uri>/', views.addDatabase, name='add_database_page'),
]
