from .models import Event
from django.contrib import admin


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'event_date', 'start_time')
    readonly_fields = ('created_at',)


admin.site.register(Event, EventAdmin)
