from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Dashboard(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="dashboard"
    )
    username = models.CharField(max_length=100)
    registration_date = models.DateField()
    last_access = models.DateTimeField(default=timezone.now)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    earned_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_withdrawal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    total_withdrawal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    active_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard for {self.username}"

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"
        ordering = ["-created_at"]  # newest first
