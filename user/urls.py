from django.urls import path


from .views import (
    UserLoginView, UserLogoutView,
    UserPasswordChangeView, UserChangeInfoView,
    UserRegisterView, UserRegisterDoneView,
    UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView,
    UserDeleteView,
    profile, user_activate
)


app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('profile/change/', UserChangeInfoView.as_view(), name='profile_change'),
    path('profile/delete/', UserDeleteView.as_view(), name='profile_delete'),
    path('profile/', profile, name='profile'),

    path('password/change/', UserPasswordChangeView.as_view(), name='password_change'),

    path('password/reset/confirm/<str:uidb64>/<str:token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),

    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', UserRegisterDoneView.as_view(), name='register_done'),
    path('register/', UserRegisterView.as_view(), name='register'),
]
