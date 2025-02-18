from django.urls import path, include
from .views import ReferralView

app_name = "referrals"

urlpatterns = [
    path("", ReferralView.as_view(), name="referral-view"),
]
