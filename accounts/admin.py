from django.contrib import admin
from .models import User, PaymentAccounts, AdminPaymentAccounts

admin.site.register(User)
admin.site.register(PaymentAccounts)
admin.site.register(AdminPaymentAccounts)
