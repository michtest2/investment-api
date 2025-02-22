# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone
# from dashboard.models import Dashboard
# from investments.models import Investment
# from .serializers import DashboardSerializer
# from referrals.models import Referral


# class DashboardView(APIView):
#     """
#     API view to retrieve the authenticated user's dashboard data.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         try:
#             dashboard = Dashboard.objects.get(user=request.user)
#             investments = Investment.objects.filter(
#                 user=request.user, is_active=True, status="active"
#             )

#             total_earned = 0
#             print(investments)
#             for investment in investments:
#                 days_passed = (
#                     timezone.now().date() - investment.start_date.date()
#                 ).days
#                 # days_passed = (timezone.now().date() - investment.start_date).days
#                 calculated_total_earned = days_passed * investment.daily_profit

#                 # Update investment total_earned if needed
#                 if investment.total_earned < calculated_total_earned:
#                     investment.total_earned = calculated_total_earned
#                     investment.save(update_fields=["total_earned"])

#                 total_earned += calculated_total_earned
#             # get all referrals buy user and total the commission earned
#             referrals = Referral.objects.filter(referrer=request.user)
#             total_commission_earned = 0
#             for referral in referrals:
#                 total_commission_earned += referral.commission_earned

#             total_earned += total_commission_earned
#             # Update dashboard
#             if dashboard.earned_total < total_earned:
#                 earned_difference = total_earned - dashboard.earned_total
#                 dashboard.earned_total = total_earned
#                 dashboard.account_balance += earned_difference
#                 dashboard.save(update_fields=["earned_total", "account_balance"])

#             dashboard.last_access = timezone.now()
#             dashboard.save(update_fields=["last_access"])

#             # Serialize the dashboard data
#             serializer = DashboardSerializer(dashboard)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Dashboard.DoesNotExist:
#             return Response(
#                 {"detail": "Dashboard not found for this user."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

# dashboard/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum

from dashboard.models import Dashboard, MonthlyRecord
from investments.models import Investment
from referrals.models import Referral
from .serializers import DashboardSerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            dashboard = Dashboard.objects.get(user=request.user)
            investments = Investment.objects.filter(
                user=request.user, is_active=True, status="active"
            )

            # 1) Calculate total_earned from active investments
            total_earned = 0
            for investment in investments:
                days_passed = (
                    timezone.now().date() - investment.start_date.date()
                ).days
                calculated_total_earned = days_passed * investment.daily_profit

                if investment.total_earned < calculated_total_earned:
                    investment.total_earned = calculated_total_earned
                    investment.save(update_fields=["total_earned"])

                total_earned += calculated_total_earned

            # 2) Add referral commissions
            referrals = Referral.objects.filter(referrer=request.user)
            total_commission_earned = sum(r.commission_earned for r in referrals)
            total_earned += total_commission_earned

            # 3) Update the Dashboard model (cumulative total)
            if dashboard.earned_total < total_earned:
                earned_difference = total_earned - dashboard.earned_total
                dashboard.earned_total = total_earned
                dashboard.account_balance += earned_difference
                dashboard.save(update_fields=["earned_total", "account_balance"])

            # Update last_access
            dashboard.last_access = timezone.now()
            dashboard.save(update_fields=["last_access"])

            # 4) Handle monthly snapshot
            today = timezone.now().date()
            current_month = today.replace(day=1)

            # Get the latest record for this user (ordered by month desc)
            latest_record = (
                MonthlyRecord.objects.filter(user=request.user)
                .order_by("-month")
                .first()
            )

            # If no record or the latest record is for a past month, create a new monthly record
            if not latest_record or latest_record.month < current_month:
                # Sum of all monthly totals so far
                previous_months_sum = (
                    MonthlyRecord.objects.filter(user=request.user)
                    .aggregate(total=Sum("total_earned"))
                    .get("total")
                    or 0
                )

                # The new month's total = dashboard's cumulative minus all previous monthly totals
                this_month_earned = dashboard.earned_total - previous_months_sum

                MonthlyRecord.objects.create(
                    user=request.user,
                    month=current_month,
                    account_balance=dashboard.account_balance,
                    total_earned=this_month_earned,  # monthly total
                )

            else:
                # The latest record is for the current month, so update it
                # Exclude the current month's record from the sum, so we only get "previous" months
                previous_months_sum = (
                    MonthlyRecord.objects.filter(user=request.user)
                    .exclude(pk=latest_record.pk)
                    .aggregate(total=Sum("total_earned"))
                    .get("total")
                    or 0
                )

                this_month_earned = dashboard.earned_total - previous_months_sum

                latest_record.account_balance = dashboard.account_balance
                latest_record.total_earned = this_month_earned  # monthly total
                latest_record.save()

            # 5) Return the serialized dashboard (including monthly records)
            serializer = DashboardSerializer(dashboard)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dashboard.DoesNotExist:
            return Response(
                {"detail": "Dashboard not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
