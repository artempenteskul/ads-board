from django.urls import path

from .views import home, about, index, other_page


app_name = 'advert'

urlpatterns = [
    path('<str:page>/', other_page, name='other'),
    path('/', index, name='index'),
    path('home/', home, name='home'),
    path('about/', about, name='about')
]
