from django.urls import path

from .views import index

app_name = 'advert'

urlpatterns = [
    path('', index, name='index'),
]
