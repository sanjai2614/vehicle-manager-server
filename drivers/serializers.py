from rest_framework import serializers

from .models import Driver


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        
        fields = [
            "id",
            "driver_name",
            "age",
            "email",
            "phone_number",
            "profile_avatar",
            "license_number",
            "vehicle_number",
            "created_at",
            "updated_at",
        ]
          
        read_only_fields=[
            "id",
            "created_at",
            "updated_at",            
        ]
