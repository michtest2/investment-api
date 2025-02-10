from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Dashboard
from .serializers import DashboardSerializer


class DashboardView(APIView):
    """
    API view to retrieve the authenticated user's dashboard data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch the dashboard data for the authenticated user
        try:
            dashboard = Dashboard.objects.get(user=request.user)
        except Dashboard.DoesNotExist:
            return Response(
                {"detail": "Dashboard not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the dashboard data
        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data, status=status.HTTP_200_OK)
