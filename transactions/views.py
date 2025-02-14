from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Withdrawal, Transaction
from .serializers import WithdrawalSerializer

from dashboard.models import Dashboard


class RequestWithdrawalView(APIView):
    """
    API view to request a withdrawal.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        pending_withdrawal_exists = Withdrawal.objects.filter(
            user=user, status="pending"
        ).exists()

        if pending_withdrawal_exists:
            return Response(
                {
                    "detail": "A pending withdrawal request is still waiting for approval. Please wait until it is approved before creating a new withdrawal requeat."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and create the withdrawal
        serializer = WithdrawalSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            withdrawal = serializer.save()
            transaction = Transaction.objects.create(
                user=user,
                type=Transaction.TransactionType.WITHDRAWAL,
                amount=withdrawal.amount,
                currency=withdrawal.currency,
                status=Transaction.TransactionStatus.PENDING,
                description=f"Withdrawal request for {withdrawal.amount} {withdrawal.currency}",
            )
            # Link the transaction to the withdrawal
            withdrawal.transaction = transaction
            withdrawal.save()
            # get user dashboard and add the withdrawal amt to it as "pending withdrwal"
            dashboard = Dashboard.objects.get(user=request.user)
            dashboard.pending_withdrawal = withdrawal.amount
            dashboard.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingWithdrawalsView(APIView):
    """
    API view to retrieve pending withdrawals for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch pending withdrawals for the authenticated user
        pending_withdrawals = Withdrawal.objects.filter(
            user=request.user, status="pending"
        )
        serializer = WithdrawalSerializer(pending_withdrawals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WithdrawalHistoryView(APIView):
    """
    API view to retrieve withdrawal history for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all withdrawals for the authenticated user
        withdrawal_history = Withdrawal.objects.filter(user=request.user)
        serializer = WithdrawalSerializer(withdrawal_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Deposit
from .serializers import DepositSerializer, DepositViewSerializer

from dashboard.models import Dashboard


class CreateDepositView(APIView):
    """
    API view to create a deposit request.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check if the user has any pending deposit.
        # This assumes that the Deposit model is linked to a Transaction via a foreign key
        # and that a deposit is pending if its transaction's status is PENDING.
        pending_deposit_exists = Deposit.objects.filter(
            user=request.user, status="pending"
        ).exists()

        if pending_deposit_exists:
            return Response(
                {
                    "detail": "A pending deposit is still waiting for approval. Please wait until it is approved before creating a new deposit."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Pass the authenticated user as part of the context
        print(request.data["plan_name"])
        serializer = DepositSerializer(
            data=request.data,
            context={"user": request.user, "plan_name": request.data["plan_name"]},
        )
        if serializer.is_valid():
            # serializer.save()
            deposit = serializer.save()
            transaction = Transaction.objects.create(
                user=request.user,
                type=Transaction.TransactionType.DEPOSIT,
                amount=deposit.amount,
                currency=deposit.currency,
                status=Transaction.TransactionStatus.PENDING,
                description=f"Withdrawal request for {deposit.amount} {deposit.currency}",
            )
            # Link the transaction to the withdrawal
            deposit.transaction = transaction
            deposit.save()
            # get user dashboard and add deposit amt to it as "active deposit"
            dashboard = Dashboard.objects.get(user=request.user)
            dashboard.active_deposit = deposit.amount
            dashboard.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingDepositsView(APIView):
    """
    API view to retrieve pending deposits for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch pending deposits for the authenticated user
        pending_deposits = Deposit.objects.filter(user=request.user, status="pending")
        serializer = DepositViewSerializer(pending_deposits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepositHistoryView(APIView):
    """
    API view to retrieve deposit history for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all deposits for the authenticated user
        deposit_history = Deposit.objects.filter(user=request.user)
        serializer = DepositViewSerializer(deposit_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
