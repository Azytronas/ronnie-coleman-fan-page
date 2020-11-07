from . import views
from django.urls import path

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:song_name>', views.details, name='details'),
]
