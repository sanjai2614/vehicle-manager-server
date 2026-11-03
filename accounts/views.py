from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from accounts.utils import set_refresh_token_cookie
from .models import User

from .serializers import RegisterSerializer


# register
@api_view(["POST"])
@permission_classes([AllowAny])
def register(req):
    serializer = RegisterSerializer(data=req.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Registration success",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login
@api_view(["POST"])
@permission_classes([AllowAny])
def login(req):

    email = req.data.get("email")
    password = req.data.get("password")

    try:
        user_obj = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        user_obj = None

    user = None

    if user_obj:
        user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return Response(
            {"success": False, "message": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # refresh, access token generate
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    response = Response(
        {
            "success": True,
            "message": "Login success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "access": access_token,
        },
        status=status.HTTP_200_OK,
    )

    return set_refresh_token_cookie(response, refresh)


# logout
@api_view(["POST"])
def logout(req):

    refresh_token = req.COOKIES.get("vehicle_refresh")

    if not refresh_token:
        response = Response(
            {"success": False, "message": "refresh token not found"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        response.delete_cookie(key="vehicle_refresh", path="/api/")

        return response

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response(
            {"success": True, "message": "Logout success"}, status=status.HTTP_200_OK
        )

        response.delete_cookie(key="vehicle_refresh", path="/api/")

        return response

    except TokenError:

        response = Response(
            {"success": False, "message": "Invalid or expires refresh token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
        response.delete_cookie(key="vehicle_refresh", path="/api/")

        return response


# refresh token
@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(req):

    refresh = req.COOKIES.get("vehicle_refresh")

    if not refresh:
        return Response(
            {"success": False, "message": "Refresh token not found"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        refresh = RefreshToken(refresh)

        # generate new access token
        access_token = str(refresh.access_token)

        response = Response(
            {
                "success": True,
                "message": "Token refreshed success",
                "access": access_token,
            },
            status=status.HTTP_200_OK,
        )

        return response

    except TokenError:

        response = Response(
            {"success": False, "message": "Invalid or expired refresh token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        response.delete_cookie(key="vehicle_refresh", path="/api/")

        return response
    

# current user
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user(req):
    user = req.user

    return Response(
        {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
        },
        status=status.HTTP_200_OK,
    )
