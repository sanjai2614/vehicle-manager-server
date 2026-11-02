from django.conf import settings


def set_refresh_token_cookie(response, refresh_token):

    response.set_cookie(
        key="vehicle_refresh",
        value=str(refresh_token),
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        max_age=7 * 24 * 60 * 60,
        path="/api/",
    )
    return response
