from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Referral


class ReferralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        referrals = Referral.objects.filter(referrer=request.user)
        return Response(
            {
                "total_referrals": referrals.count(),
                "active_referrals": referrals.filter(status="Active").count(),
                "total_commission": sum(r.commission_earned for r in referrals),
                "commission_rate": "7",
                "referral_code": (
                    request.user.referrals.first().referral_code
                    if request.user.referrals.exists()
                    else ""
                ),
                "referral_history": [
                    {
                        "username": (
                            r.referred_user.username if r.referred_user else "Pending"
                        ),
                        "date": r.created_at.date(),
                        "status": r.status,
                        "commission": r.commission_earned,
                    }
                    for r in referrals
                ],
            }
        )
