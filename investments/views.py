from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InvestmentPlan
from .serializers import InvestmentPlanSerializer


class InvestmentPlanListView(APIView):
    """
    API view to retrieve all investment plans ordered by daily ROI (highest first).
    """

    def get(self, request, *args, **kwargs):
        investment_plans = InvestmentPlan.objects.filter(is_active=True).order_by(
            "daily_roi"
        )
        serializer = InvestmentPlanSerializer(investment_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InvestmentPlan
from .serializers import InvestmentPlanSerializer
import uuid


class InvestmentPlanDetailView(APIView):
    """
    API view to retrieve a specific investment plan by its UUID.
    """

    def get(self, request, *args, **kwargs):
        # Get the plan UUID from the URL
        plan_id = kwargs.get("plan_id")

        try:
            # Convert the plan_id to UUID type
            # plan_uuid = uuid.UUID(plan_id)

            # Fetch the investment plan by its UUID
            investment_plan = InvestmentPlan.objects.get(id=plan_id, is_active=True)
        except (InvestmentPlan.DoesNotExist, ValueError):
            return Response(
                {"detail": "Investment plan not found or is inactive."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the plan data
        serializer = InvestmentPlanSerializer(investment_plan)

        # Return the plan details
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Investment
from .serializers import InvestmentSerializer


class ActiveInvestmentsView(APIView):
    """
    API view to retrieve active investments for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch active investments for the authenticated user
        active_investments = Investment.objects.filter(
            user=request.user, is_active=True
        )
        serializer = InvestmentSerializer(active_investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvestmentHistoryView(APIView):
    """
    API view to retrieve investment history for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all investments for the authenticated user
        investment_history = Investment.objects.filter(user=request.user)
        serializer = InvestmentSerializer(investment_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvestmentDetailView(APIView):
    """
    API view to retrieve details of a specific investment for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the investment ID from the URL
        investment_id = kwargs.get("id")

        try:
            # Fetch the investment for the authenticated user
            investment = Investment.objects.get(id=investment_id, user=request.user)
        except Investment.DoesNotExist:
            return Response(
                {
                    "detail": "Investment not found or you do not have permission to view it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the investment data
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)
