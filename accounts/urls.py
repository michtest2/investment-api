from django.urls import path
from .views import AccountSettingsView, PaymentAccountsView


app_name = "accounts"

urlpatterns = [
    path("settings", AccountSettingsView.as_view(), name="account-settings"),
    path("payment_account", PaymentAccountsView.as_view(), name="payment-account"),
]
