from django.urls import path


from .views import other_page


app_name = 'common'

urlpatterns = [
    path('<str:page>/', other_page, name='other'),
]
