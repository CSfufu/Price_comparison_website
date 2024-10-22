# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, LogoutView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('me/', UserDetailView.as_view(), name='api_me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

