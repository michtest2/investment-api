from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class InvestmentStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    TERMINATED = "terminated", "Terminated"


class InvestmentPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # e.g., "Starter contract plan"
    daily_roi = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 1.5%
    minimum_deposit = models.DecimalField(max_digits=15, decimal_places=2)
    maximum_deposit = models.DecimalField(max_digits=15, decimal_places=2)
    duration_days = models.PositiveIntegerField()  # Duration in days
    referral_commission = models.DecimalField(
        max_digits=5, decimal_places=2
    )  # Percentage
    is_active = models.BooleanField(default=True)  # Whether the plan is active
    description = models.TextField()  # Detailed description of the plan
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Investment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="investments")
    plan = models.ForeignKey(
        InvestmentPlan, on_delete=models.CASCADE, related_name="investments"
    )
    is_active = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=InvestmentStatus.choices, default=InvestmentStatus.ACTIVE
    )
    total_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    last_payout_date = models.DateTimeField(blank=True, null=True)
    daily_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.amount}"
