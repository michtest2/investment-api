from rest_framework import serializers
from .models import Dashboard


class DashboardSerializer(serializers.ModelSerializer):
    registration_date = serializers.DateField(format="%b-%d-%Y")
    last_access = serializers.DateTimeField(format="%b-%d-%Y %I:%M:%S %p")

    class Meta:
        model = Dashboard
        fields = [
            "username",
            "registration_date",
            "last_access",
            "account_balance",
            "earned_total",
            "pending_withdrawal",
            "total_withdrawal",
            "active_deposit",
        ]
