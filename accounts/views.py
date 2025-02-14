from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

from .serializers import (
    UserSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)

from django.contrib.auth import get_user_model

from dashboard.models import Dashboard
from .models import PaymentAccounts
from dashboard.serializers import DashboardSerializer
from django.utils import timezone

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            # Create user
            user = user_serializer.save()
            user.set_password(user_serializer.validated_data["password"])
            user.save()

            # Create dashboard
            dashboard = Dashboard.objects.create(
                user=user,
                username=user.username,
                registration_date=timezone.now().date(),
                last_access=timezone.now(),
                account_balance=0.00,
                earned_total=0.00,
                pending_withdrawal=0.00,
                total_withdrawal=0.00,
                active_deposit=0.00,
            )
            payment_accounts = PaymentAccounts.objects.create(user=user)

            # Serialize the data
            user_data = UserSerializer(user).data
            dashboard_data = DashboardSerializer(dashboard).data

            # Return combined dictionary
            return Response(
                {"user": user_data, "dashboard": dashboard_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Get refresh token from cookie
            refresh_token = request.COOKIES.get(
                settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]
            )

            if refresh_token:
                # Blacklist the token
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response(
                {"message": "logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )

            # Delete cookies
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])

            return response

        except Exception as e:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


import os
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from .serializers import PasswordResetSerializer

# from .models import User


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)

                # Create context for email template
                context = {
                    "user": user,
                    "reset_url": f"https://yourfrontend.com/reset-password?token={token}?email={email}",
                    "valid_hours": 24,
                }

                # Render email template
                html_message = render_to_string(
                    "accounts/password_reset_email.html",  # Make sure this path is correct
                    context,
                )
                print(html_message)
                # Create plain text version
                plain_message = html_message
                # strip_tags(html_message)

                # Configure MailerSend SMTP settings
                subject = "Reset Your Password"
                recipient_list = [email]
                from_email = settings.DEFAULT_FROM_EMAIL

                try:
                    with get_connection(
                        host=settings.MAILERSEND_SMTP_HOST,
                        port=settings.MAILERSEND_SMTP_PORT,
                        username=settings.MAILERSEND_SMTP_USERNAME,
                        password=settings.MAILERSEND_API_KEY,
                        use_tls=True,
                    ) as connection:
                        email = EmailMessage(
                            subject=subject,
                            body=plain_message,
                            to=recipient_list,
                            from_email=from_email,
                            connection=connection,
                        )
                        email.content_subtype = "html"  # Set the content type to HTML
                        email.send()

                    return Response(
                        {"message": "Password reset email sent"},
                        status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    print(f"Email sending error: {str(e)}")  # Add this for debugging
                    return Response(
                        {"error": "Failed to send email"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            except User.DoesNotExist:
                # Don't reveal if email exists
                return Response(
                    {
                        "message": "If an account exists with this email, a password reset link has been sent."
                    },
                    status=status.HTTP_200_OK,
                )


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=request.data.get("email"))
                # user = request.user
                if default_token_generator.check_token(
                    user, serializer.validated_data["token"]
                ):
                    user.set_password(serializer.validated_data["new_password"])
                    user.save()
                    return Response({"message": "Password has been reset"})
                return Response(
                    {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, PaymentAccounts, AdminPaymentAccounts
from .serializers import UserSerializer, PaymentAccountsSerializer


class AccountSettingsView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can access this view

    def get(self, request):
        """
        Retrieve the authenticated user's details and their payment accounts.
        """
        user = request.user
        user_serializer = UserSerializer(user)

        # try:
        #     payment_account = PaymentAccounts.objects.get(user=user)
        #     payment_serializer = PaymentAccountsSerializer(payment_account)
        # except PaymentAccounts.DoesNotExist:
        #     payment_serializer = None

        response_data = {
            "user": user_serializer.data,
            # "payment_account": payment_serializer.data if payment_serializer else None,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update the authenticated user's details.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentAccountsView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can access this view

    def get(self, request):
        """
        Retrieve the authenticated user's payment account details.
        """
        user = request.user
        try:
            payment_account = PaymentAccounts.objects.get(user=user)
            serializer = PaymentAccountsSerializer(payment_account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaymentAccounts.DoesNotExist:
            return Response(
                {"detail": "Payment account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request):
        """
        Update the authenticated user's payment account details.
        """
        user = request.user
        try:
            payment_account = PaymentAccounts.objects.get(user=user)
        except PaymentAccounts.DoesNotExist:
            return Response(
                {"detail": "Payment account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PaymentAccountsSerializer(
            payment_account, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# accounts/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            tokens = response.data
            response = Response(
                {
                    "message": "Login successful",
                    # "user": request.user.username,  # or any other user data you want to return
                }
            )

            # Set cookies
            response.set_cookie(
                settings.SIMPLE_JWT["AUTH_COOKIE"],
                tokens["access"],
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            )

            response.set_cookie(
                settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                tokens["refresh"],
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            )
        return response


class AdminPaymentAccountsView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can access this view

    def get(self, request):
        """
        Retrieve admin payment account details.
        """
        # user = request.user
        try:
            payment_account = AdminPaymentAccounts.objects.all()
            serializer = PaymentAccountsSerializer(payment_account, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaymentAccounts.DoesNotExist:
            return Response(
                {"detail": "Admin Payment account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MeUserSerializer  # You'll need to create this


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
