from django.urls import path

from . import views

# Create your ulrs here.

app_name = 'core'

urlpatterns = [
    path('', views.login, name='login_page'),
    path('home/', views.home, name='home_page'),
]
