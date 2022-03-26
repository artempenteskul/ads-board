from django.urls import path

from . import views

app_name = 'advert'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.AdvertLoginView.as_view(), name='login'),
    path('logout/', views.AdvertLogout.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change/', views.ChangeUserInfoView.as_view(), name='profile-change'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('<str:page>/', views.other_page, name='other'),
]
