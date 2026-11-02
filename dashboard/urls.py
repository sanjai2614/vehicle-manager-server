from django.urls import path
from .views import get_all_drivers, get_users, update_user_status, get_deleted_drivers

urlpatterns = [
    path("users/", get_users, name="get_users"),
    path("users/<int:pk>/status/", update_user_status, name="update_user_status"),
    path("drivers/", get_all_drivers, name="get_all_drivers"),
    path(
    "deleted-drivers/",
    get_deleted_drivers,
    name="get_deleted_drivers"
),
]
