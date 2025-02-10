from django.db import models
import uuid
from django.conf import settings
from investments.models import InvestmentPlan


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAWAL = "withdrawal", "Withdrawal"
        INVESTMENT = "investment", "Investment"
        REFERRAL = "referral", "Referral"
        PROFIT = "profit", "Profit"

    class TransactionStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    currency = models.CharField(max_length=10)  # e.g., 'USD', 'BTC', 'USDT'
    transaction_hash = models.CharField(
        max_length=255, blank=True, null=True
    )  # Optional
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return (
            f"{self.user} -{self.type} - {self.amount} {self.currency} ({self.status})"
        )


class WithdrawalStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    COMPLETED = "completed", "Completed"


class DepositStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    FAILED = "failed", "Failed"


class Withdrawal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="withdrawals"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10)
    wallet_address = models.CharField(max_length=255)
    wallet_address_type = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=WithdrawalStatus.choices,
        default=WithdrawalStatus.PENDING,
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="withdrawals",
        blank=True,
        null=True,
    )
    rejection_reason = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency} ({self.status})"


class Deposit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deposits"
    )
    plan = models.ForeignKey(
        InvestmentPlan,
        on_delete=models.CASCADE,
        related_name="deposits",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=255)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="deposits",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=10, choices=DepositStatus.choices, default=DepositStatus.PENDING
    )
    proof_of_payment = models.CharField(max_length=255, blank=True, null=True)
    confirmation_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency} ({self.status})"
