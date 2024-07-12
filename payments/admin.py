from .models import Payment
from django.contrib import admin


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'ticket_purchased', 'paid_at')


admin.site.register(Payment, PaymentAdmin)