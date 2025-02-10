from django.urls import path
from .views import (
    RequestWithdrawalView,
    PendingWithdrawalsView,
    WithdrawalHistoryView,
    CreateDepositView,
    PendingDepositsView,
    DepositHistoryView,
)

app_name = "transactions"
urlpatterns = [
    # withdrawals
    path(
        "withdrawals/request",
        RequestWithdrawalView.as_view(),
        name="request-withdrawal",
    ),
    path(
        "withdrawals/pending",
        PendingWithdrawalsView.as_view(),
        name="pending-withdrawals",
    ),
    path(
        "withdrawals/history",
        WithdrawalHistoryView.as_view(),
        name="withdrawal-history",
    ),
    # deposits
    path("deposits/create", CreateDepositView.as_view(), name="create-deposit"),
    path("deposits/pending", PendingDepositsView.as_view(), name="pending-deposits"),
    path("deposits/history", DepositHistoryView.as_view(), name="deposit-history"),
]
