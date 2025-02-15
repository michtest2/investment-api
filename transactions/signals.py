from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Deposit, Withdrawal
from investments.models import Investment
from dashboard.models import Dashboard


@receiver(post_save, sender=Deposit, dispatch_uid="deposit_reviewed")
def deposit_reviewed(sender, instance, created, **kwargs):
    if not created and instance.status == "confirmed":
        print("signal call working", instance.status)

        # Only proceed if we have a plan associated with the deposit
        if not instance.plan:
            print("No investment plan associated with deposit")
            return

        # Calculate investment dates
        start_date = timezone.now()
        # Assuming plan duration is stored in days
        end_date = start_date + timedelta(days=instance.plan.duration_days)

        # Calculate daily profit based on plan's ROI
        # Assuming ROI is stored as a percentage (e.g., 15 for 15%)
        daily_profit = instance.amount * (instance.plan.daily_roi / 100)

        # Create new investment
        try:
            investment = Investment.objects.create(
                user=instance.user,
                plan=instance.plan,
                amount=instance.amount,
                start_date=start_date,
                end_date=end_date,
                status="ACTIVE",
                daily_profit=daily_profit,
                is_active=True,
            )

            print(f"Investment created successfully: {investment.id}")

            # Update the deposit with confirmation time if not already set
            if not instance.confirmation_time:
                instance.confirmation_time = timezone.now()
                instance.save(update_fields=["confirmation_time"])

            # update dashboard active_deposit and balance
            dashboard = Dashboard.objects.get(user=instance.user)
            dashboard.active_deposit = 0  # dashboard.active_deposit - instance.amount
            dashboard.account_balance += instance.amount
            dashboard.save()

        except Exception as e:
            print(f"Error creating investment: {str(e)}")


@receiver(post_save, sender=Withdrawal, dispatch_uid="withdrawal_reviewed")
def withdrawal_reviewed(sender, instance, created, **kwargs):
    if not created and instance.status == "approved":
        print("Withdrawal signal working", instance.status)

        try:
            # Update dashboard total_withdrawal and balance
            dashboard = Dashboard.objects.get(user=instance.user)

            # Increase total withdrawal
            dashboard.total_withdrawal = dashboard.total_withdrawal + instance.amount
            dashboard.pending_withdrawal = (
                dashboard.pending_withdrawal - instance.amount
            )
            # Decrease account balance
            dashboard.account_balance = dashboard.account_balance - instance.amount

            # Save dashboard changes
            dashboard.save()

            # Update withdrawal confirmation time if not already set
            if not instance.confirmation_time:
                instance.confirmation_time = timezone.now()
                instance.save(update_fields=["confirmation_time"])

            print(f"Dashboard updated successfully for withdrawal: {instance.id}")

        except Dashboard.DoesNotExist:
            print(f"Dashboard not found for user: {instance.user.id}")
        except Exception as e:
            print(f"Error processing withdrawal: {str(e)}")
