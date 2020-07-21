from django.urls import path

from . import views

# Create yours urls here.

app_name = 'collector'

urlpatterns = [
    path('search_artist', views.search_artist, name='search_artist_page')
]
