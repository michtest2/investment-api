from django.urls import path
from .views import AccountSettingsView, PaymentAccountsView, AdminPaymentAccountsView


app_name = "accounts"

urlpatterns = [
    path("settings", AccountSettingsView.as_view(), name="account-settings"),
    path("payment_account", PaymentAccountsView.as_view(), name="payment-account"),
    path(
        "payment_account/admin",
        AdminPaymentAccountsView.as_view(),
        name="payment-account",
    ),
]

# http://127.0.0.1:8000/api/v1/accounts/payment_account/admin
