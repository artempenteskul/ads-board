from django.urls import path


from .views import index, other_page


app_name = 'common'

urlpatterns = [
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
