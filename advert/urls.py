from django.urls import path

from .views import by_rubric


app_name = 'advert'

urlpatterns = [
    path('<int:pk>/', by_rubric, name='by_rubric'),
]
