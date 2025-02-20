from rest_framework import serializers
from .models import Dashboard
from referrals.models import Referral


class DashboardSerializer(serializers.ModelSerializer):
    registration_date = serializers.DateField(format="%b-%d-%Y")
    last_access = serializers.DateTimeField(format="%b-%d-%Y %I:%M:%S %p")
    referrals_count = serializers.SerializerMethodField()

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
            "referrals_count",
        ]

    # get count of referrals
    def get_referrals_count(self, obj):
        # get user from obj, get user referrals and count them
        return Referral.objects.filter(referrer=obj.user).count()
