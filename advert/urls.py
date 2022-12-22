from django.urls import path

from .views import index, by_rubric, detail, add_ad, change_ad, delete_ad


app_name = 'advert'

urlpatterns = [
    path('', index, name='index'),
    path('advert/add/', add_ad, name='add_ad'),
    path('advert/change/<int:pk>/', change_ad, name='change_ad'),
    path('advert/delete/<int:pk>/', delete_ad, name='delete_ad'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
]
