from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Referral(models.Model):
    referrer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referrals"
    )
    referred_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="referred_by",
        null=True,
        blank=True,
    )
    referral_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
    )
    commission_earned = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.username} refer {self.referred_user.username}-> {self.referral_code}"
