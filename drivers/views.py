from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Driver
from .serializers import DriverSerializer
from .utils import upload_driver_avatar, delete_driver_avatar
from cloudinary.uploader import destroy


# Create driver
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_driver(req):

    data = req.data.copy()

    image = req.FILES.get("profile_avatar")

    if image:
        try:
            result = upload_driver_avatar(image)

            data["profile_avatar"] = result["url"]

            serializer = DriverSerializer(data=data)

            if serializer.is_valid():
                serializer.save(
                    user=req.user, profile_avatar_public_id=result["public_id"]
                )

                return Response(
                    {
                        "success": True,
                        "message": "Driver created success",
                        "driver": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            destroy(result["public_id"])

            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as error:
            return Response(
                {
                    "success": False,
                    "message": "Image upload failed",
                    "error": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    serializer = DriverSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=req.user)

        return Response(
            {
                "success": True,
                "message": "Driver created success",
                "driver": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {"success": False, "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# get drivers
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_drivers(req):

    # get all active drivers
    drivers = Driver.objects.filter(is_deleted=False)

    # get particular user drivers
    if req.user.role != "admin":
        drivers = drivers.filter(user=req.user)

    serializer = DriverSerializer(drivers, many=True)

    return Response(
        {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
    )


# Get a specific driver
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_driver(req, pk):

    drivers = Driver.objects.filter(is_deleted=False)

    if req.user.role != "admin":
        drivers = drivers.filter(user=req.user)

    driver = get_object_or_404(drivers, pk=pk)

    serializer = DriverSerializer(driver)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


# Update a specific driver
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_driver(req, pk):

    drivers = Driver.objects.filter(is_deleted=False)

    if req.user.role != "admin":
        drivers = drivers.filter(user=req.user)

    driver = get_object_or_404(drivers, pk=pk)

    data = req.data.copy()
    image = req.FILES.get("profile_avatar")

    new_public_id = None

    if image:
        try:
            result = upload_driver_avatar(image)

            data["profile_avatar"] = result["url"]
            new_public_id = result["public_id"]

        except Exception:
            return Response(
                {"success": False, "message": "Image upload failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    serializer = DriverSerializer(driver, data=data, partial=True)

    if serializer.is_valid():

        old_public_id = driver.profile_avatar_public_id

        if new_public_id:
            serializer.save(profile_avatar_public_id=new_public_id)

            if old_public_id:
                delete_driver_avatar(old_public_id)

        else:
            serializer.save()

        return Response(
            {
                "success": True,
                "message": "Driver updated success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    if new_public_id:
        delete_driver_avatar(new_public_id)

    return Response(
        {"success": False, "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# Soft delete a specific driver
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_driver(req, pk):

    drivers = Driver.objects.filter(is_deleted=False)

    if req.user.role != "admin":
        drivers = drivers.filter(user=req.user)

    driver = get_object_or_404(drivers, pk=pk)

    driver.is_deleted = True
    driver.save()

    return Response(
        {"success": True, "message": "Driver deleted success"},
        status=status.HTTP_200_OK,
    )
