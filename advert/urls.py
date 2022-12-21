from django.urls import path

from .views import by_rubric, detail


app_name = 'advert'

urlpatterns = [
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
]
