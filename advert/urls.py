from django.urls import path

from .views import hello

app_name = 'advert'

urlpatterns = [
    path('hello/', hello, name='hello'),
]
