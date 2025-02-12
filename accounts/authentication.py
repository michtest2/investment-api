# accounts/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        if header is None:
            return None

        # Modify the request to include the token in the header
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {header}"

        return super().authenticate(request)
