from django.urls import path

from .views import index, other_page, AdvertLoginView, AdvertLogout, profile

app_name = 'advert'

urlpatterns = [
    path('', index, name='index'),
    path('login/', AdvertLoginView.as_view(), name='login'),
    path('logout/', AdvertLogout.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('<str:page>/', other_page, name='other'),
]
