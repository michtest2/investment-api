from django.urls import path, include
from .views import (
    InvestmentPlanListView,
    InvestmentPlanDetailView,
    ActiveInvestmentsView,
    InvestmentHistoryView,
    InvestmentDetailView,
)
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "investments"
urlpatterns = [
    path("plans/", InvestmentPlanListView.as_view(), name="plans_list"),
    path(
        "plans/<uuid:plan_id>/",
        InvestmentPlanDetailView.as_view(),
        name="investment-plan-detail",
    ),
    path(
        "active",
        ActiveInvestmentsView.as_view(),
        name="active-investments",
    ),
    path(
        "history",
        InvestmentHistoryView.as_view(),
        name="investment-history",
    ),
    path(
        "<uuid:id>",
        InvestmentDetailView.as_view(),
        name="investment-detail",
    ),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#for saving the pics
