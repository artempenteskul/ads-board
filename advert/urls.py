from django.urls import path

from .views import (
    index, other_page, profile,
    AdsBoardLoginView, AdsBoardLogoutView, AdsBoardPasswordChangeView,
    ChangeUserInfoView, RegisterUserView, RegisterDoneView, user_activate, DeleteUserView
)

app_name = 'advert'

urlpatterns = [
    path('login/', AdsBoardLoginView.as_view(), name='login'),
    path('logout/', AdsBoardLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('password/change/', AdsBoardPasswordChangeView.as_view(), name='password_change'),
    path('profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
