from django.urls import path

from .views import home, about, index


app_name = 'advert'

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('about/', about, name='about')
]
