from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.text import slugify

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "full_name",
            "phone_number",
            "account_status",
            "is_email_verified",
            "two_factor_enabled",
            # "account_balance",
            "referral_code",
            "referred_by",
            "preferred_language",
            "created_at",
            "updated_at",
            "password",
            "password2",
        )
        read_only_fields = ("account_balance", "created_at", "updated_at")

    # def validate(self, attrs):
    #     if attrs["password"] != attrs["password2"]:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."}
    #         )
    #     return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)  # Remove password2 from data
        # Generate username from full_name
        full_name = validated_data.get("full_name", "")
        base_username = slugify(full_name.replace(" ", "_"))

        # Ensure uniqueness
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        validated_data["username"] = username

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            full_name=validated_data.get("full_name"),
            # phone_number=validated_data.get("phone_number"),
            # preferred_language=validated_data.get("preferred_language"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    token = serializers.CharField()


from .models import PaymentAccounts


class PaymentAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAccounts
        fields = [
            "id",
            "user",
            "BTC_address",
            "ETH_address",
            "LTC_address",
            "BCH_address",
            "XRP_address",
            "ADA_address",
            "DOT_address",
            "SOL_address",
            "DOGE_address",
            "USDT_address",
        ]
        read_only_fields = ["id", "user"]  # Ensure 'id' and 'user' are read-only
