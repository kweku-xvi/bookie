from .models import Ticket
from django.contrib import admin


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'event', 'price', 'quantity')
    readonly_fields = ('created_at',)

admin.site.register(Ticket, TicketAdmin)
