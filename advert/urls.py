from django.urls import path

from .views import index, other_page, AdsBoardLoginView


app_name = 'advert'

urlpatterns = [
    path('login/', AdsBoardLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
