from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from dashboard.models import Dashboard
from investments.models import Investment
from .serializers import DashboardSerializer
from referrals.models import Referral


class DashboardView(APIView):
    """
    API view to retrieve the authenticated user's dashboard data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            dashboard = Dashboard.objects.get(user=request.user)
            investments = Investment.objects.filter(
                user=request.user, is_active=True, status="active"
            )

            total_earned = 0
            print(investments)
            for investment in investments:
                days_passed = (
                    timezone.now().date() - investment.start_date.date()
                ).days
                # days_passed = (timezone.now().date() - investment.start_date).days
                calculated_total_earned = days_passed * investment.daily_profit

                # Update investment total_earned if needed
                if investment.total_earned < calculated_total_earned:
                    investment.total_earned = calculated_total_earned
                    investment.save(update_fields=["total_earned"])

                total_earned += calculated_total_earned
            # get all referrals buy user and total the commission earned
            referrals = Referral.objects.filter(referrer=request.user)
            total_commission_earned = 0
            for referral in referrals:
                total_commission_earned += referral.commission_earned

            total_earned += total_commission_earned
            # Update dashboard
            if dashboard.earned_total < total_earned:
                earned_difference = total_earned - dashboard.earned_total
                dashboard.earned_total = total_earned
                dashboard.account_balance += earned_difference
                dashboard.save(update_fields=["earned_total", "account_balance"])

            dashboard.last_access = timezone.now()
            dashboard.save(update_fields=["last_access"])

            # Serialize the dashboard data
            serializer = DashboardSerializer(dashboard)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dashboard.DoesNotExist:
            return Response(
                {"detail": "Dashboard not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
