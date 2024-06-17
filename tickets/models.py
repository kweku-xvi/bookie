import uuid
from programs.models import Event
from django.db import models


class Ticket(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.event.name} - {self.name}'

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = 'tck-' + str(uuid.uuid4())[:6]
        super().save(*args, **kwargs)


    class Meta:
        ordering = ('created_at',)