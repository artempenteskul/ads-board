from django.urls import path

from .views import home, about

app_name = 'advert'

urlpatterns = [
    path('home/', home, name='home'),
    path('about/', about, name='about')
]
