from .models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
from tickets.models import Ticket

@receiver(post_save, sender=Ticket)
def update_event_status(sender, instance, created, **kwargs):
    if created:
        event = instance.event
        event.is_active = True
        event.save()