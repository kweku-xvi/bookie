from .models import Event
from django.contrib import admin


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'venue', 'category', 'event_date', 'start_time', 'is_active')
    readonly_fields = ('created_at',)


admin.site.register(Event, EventAdmin)
