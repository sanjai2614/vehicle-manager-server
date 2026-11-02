from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from accounts.permissions import IsAdminRole
from drivers.models import Driver
from drivers.serializers import DriverSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminRole])
def get_users(req):

    users = User.objects.all().order_by("-date_joined")

    data = []

    for user in users:
        data.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "date_joined": user.date_joined,
            }
        )

    return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdminRole])
def update_user_status(req, pk):

    user = get_object_or_404(User, pk=pk)

    is_active = req.data.get("is_active")

    if not isinstance(is_active, bool):
        return Response(
            {"success": False, "message": "is_active must be true or false"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user.is_superuser:
        return Response(
            {"success": False, "message": "Cannot change superuser status"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.is_active = is_active
    user.save(update_fields=["is_active"])

    return Response(
        {
            "success": True,
            "message": "User status updated success",
            "user": {
                "id": user.id,
                "username": user.username,
                "is_active": user.is_active,
            },
        },
        status=status.HTTP_200_OK,
    )

# get active drivers
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminRole])
def get_all_drivers(req):

    drivers = Driver.objects.filter(is_deleted=False).select_related("user")

    serializer = DriverSerializer(drivers, many=True)

    return Response(
        {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
    )
    
   
# Get deleted drivers
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminRole])
def get_deleted_drivers(req):

    drivers = Driver.objects.filter(is_deleted=True)

    serializer = DriverSerializer(drivers, many=True)

    return Response(
        {
            "success": True,
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )