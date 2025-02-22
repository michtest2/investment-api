from rest_framework import serializers
from .models import Dashboard
from referrals.models import Referral


# class DashboardSerializer(serializers.ModelSerializer):
#     registration_date = serializers.DateField(format="%b-%d-%Y")
#     last_access = serializers.DateTimeField(format="%b-%d-%Y %I:%M:%S %p")
#     referrals_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Dashboard
#         fields = [
#             "username",
#             "registration_date",
#             "last_access",
#             "account_balance",
#             "earned_total",
#             "pending_withdrawal",
#             "total_withdrawal",
#             "active_deposit",
#             "referrals_count",
#         ]

#     # get count of referrals
#     def get_referrals_count(self, obj):
#         # get user from obj, get user referrals and count them
#         return Referral.objects.filter(referrer=obj.user).count()
# dashboard/serializers.py
from rest_framework import serializers
from .models import Dashboard, MonthlyRecord
from referrals.models import Referral


class MonthlyRecordSerializer(serializers.ModelSerializer):
    # Display the month as a word, e.g. "January"
    month = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyRecord
        fields = [
            "month",
            "account_balance",
            "total_earned",  # This is now "earned only in that month"
            "created_at",
            "updated_at",
        ]

    def get_month(self, obj):
        return obj.month.strftime("%b")


class DashboardSerializer(serializers.ModelSerializer):
    registration_date = serializers.DateField(format="%b-%d-%Y")
    last_access = serializers.DateTimeField(format="%b-%d-%Y %I:%M:%S %p")
    referrals_count = serializers.SerializerMethodField()
    monthly_records = serializers.SerializerMethodField()

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
            "monthly_records",
        ]

    def get_referrals_count(self, obj):
        return Referral.objects.filter(referrer=obj.user).count()

    def get_monthly_records(self, obj):
        records = MonthlyRecord.objects.filter(user=obj.user).order_by("month")
        return MonthlyRecordSerializer(records, many=True).data
