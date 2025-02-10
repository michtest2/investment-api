from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import schedule

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Create Celery app
app = Celery("investment_api")

# Load task modules from all registered Django app configs
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    "calculate-daily-roi": {
        "task": "calculate_daily_roi",
        "schedule": schedule(run_every=3),  # 86400 seconds = 1 day
    },
}
