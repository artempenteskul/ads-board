from django.urls import path

from .views import index, by_rubric, detail, add_new_ad


app_name = 'advert'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add_new_ad, name='add_new_ad'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
]
