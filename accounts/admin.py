from django.contrib import admin
from .models import User, PaymentAccounts

admin.site.register(User)
admin.site.register(PaymentAccounts)
