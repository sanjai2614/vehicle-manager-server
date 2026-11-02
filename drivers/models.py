from django.db import models
from config import settings


class Driver(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drivers"
    )

    driver_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    profile_avatar = models.URLField(blank=True, null=True)
    profile_avatar_public_id = models.CharField(
    max_length=255,
    blank=True,
    null=True
)
    license_number = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.driver_name
