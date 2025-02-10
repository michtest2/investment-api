from celery import shared_task
from django.utils import timezone
from .models import Investment
from dashboard.models import Dashboard


@shared_task(name="calculate_daily_roi")
def calculate_daily_roi():
    """
    Calculate and add daily ROI to all active investments
    """
    # Get all active investments that haven't ended
    active_investments = Investment.objects.filter(
        is_active=True,
        status="Active",
        # end_date__gt=timezone.now()
    )

    success_count = 0
    failed_count = 0

    for investment in active_investments:
        try:
            # Update total earned with daily profit
            # old_total = investment.total_earned  # Debug line
            investment.total_earned += investment.daily_profit

            dashboard = Dashboard.objects.get(user=investment.user)
            # old_balance = dashboard.account_balance  # Debug line
            # old_earned = dashboard.earned_total  # Debug line

            dashboard.account_balance += investment.daily_profit
            dashboard.earned_total += investment.daily_profit

            # # Print debug info
            # print(
            #     f"Investment {investment.id}: {old_total} -> {investment.total_earned}"
            # )
            # print(f"Dashboard balance: {old_balance} -> {dashboard.account_balance}")
            # print(f"Dashboard earned: {old_earned} -> {dashboard.earned_total}")

            # Save both objects
            investment.save(update_fields=["total_earned"])
            dashboard.save(update_fields=["account_balance", "earned_total"])

            success_count += 1
        except Exception as e:
            print(f"Failed to process ROI for investment {investment.id}: {str(e)}")
            failed_count += 1

    return f"Processed ROI for {success_count} investments. Failed: {failed_count}"
