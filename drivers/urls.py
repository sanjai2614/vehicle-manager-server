from django.urls import path

from .views import create_driver, delete_driver, get_driver, get_drivers, update_driver

urlpatterns = [
    path("", get_drivers, name="get_drivers"),
    path("create/", create_driver, name="create_driver"),
    path("<int:pk>/", get_driver, name="get_driver"),
    path("<int:pk>/update/", update_driver, name="update_driver"),
    path("<int:pk>/delete/", delete_driver, name="delete_driver"),
]
