from django.urls import path
from .views import login, logout, refresh_token, register, get_current_user

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("token/refresh/", refresh_token, name="token_refresh"),
    path("me/", get_current_user, name="current_user"),
]
