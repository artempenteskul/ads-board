from django.urls import path

from . import views

app_name = 'advert'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.AdvertLoginView.as_view(), name='login'),
    path('logout/', views.AdvertLogout.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change/', views.ChangeUserInfoView.as_view(), name='profile-change'),
    path('password/change/', views.UserPasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', views.UserPasswordResetView.as_view(), name='password-reset'),
    path('password/done/reset/', views.UserPasswordDoneResetView.as_view(), name='password-reset-done'),
    path('password/confirm/reset/', views.UserPasswordResetConfirmView.as_view(), name='password-confirm-reset'),
    path('password/complete/reset/', views.UserPasswordCompleteResetView.as_view(), name='password-complete-reset'),
    path('register/done/', views.RegisterUserDoneView.as_view(), name='register-done'),
    path('register/activate/<str:sign>/', views.user_activate, name='register-activate'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('user/delete/', views.DeleteUserView.as_view(), name='user-delete'),
    path('<str:page>/', views.other_page, name='other'),
]
