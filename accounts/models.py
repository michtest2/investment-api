from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions", blank=True
    )

    # Add additional fields
    class AccountStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        INACTIVE = "inactive", "Inactive"

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    # email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Optional
    # registration_date = models.DateTimeField(auto_now_add=True)
    last_access = models.DateTimeField(auto_now=True)
    account_status = models.CharField(
        max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE
    )
    is_email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    # account_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
         "self", on_delete=models.SET_NULL, related_name="temp_ref",blank=True, null=True
    )  # Optional
    address = models.TextField(blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default="en")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # payment_account = models.ForeignKey(
    #     PaymentAccounts, on_delete=models.CASCADE, related_name="user"
    # )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return self.email


class PaymentAccounts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_account"
    )
    BTC_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Bitcoin Address"
    )
    ETH_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Ethereum Address"
    )
    LTC_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Litecoin Address"
    )
    BCH_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Bitcoin Cash Address"
    )
    XRP_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Ripple Address"
    )
    ADA_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Cardano Address"
    )
    DOT_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Polkadot Address"
    )
    SOL_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Solana Address"
    )
    DOGE_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Dogecoin Address"
    )
    USDT_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Tether Address"
    )

    def __str__(self):
        return f"Payment Accounts for {self.user.username}"

    class Meta:
        verbose_name = "Payment Account"
        verbose_name_plural = "Payment Accounts"


class AdminPaymentAccounts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_payment_account"
    )
    BTC_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Bitcoin Address"
    )
    ETH_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Ethereum Address"
    )
    LTC_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Litecoin Address"
    )
    BCH_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Bitcoin Cash Address"
    )
    XRP_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Ripple Address"
    )
    ADA_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Cardano Address"
    )
    DOT_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Polkadot Address"
    )
    SOL_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Solana Address"
    )
    DOGE_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Dogecoin Address"
    )
    USDT_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Tether Address"
    )

    def __str__(self):
        return f"Payment Accounts for {self.user.username}"

    class Meta:
        verbose_name = "Admin Payment Account"
        verbose_name_plural = "Admin Payment Accounts"
