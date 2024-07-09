import uuid, string, random
from accounts.models import User
from programs.models import Event
from django.db import models


def generate_id(num:int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))


class TicketType(models.Model):
    ticket_type_id = models.CharField(max_length=10, primary_key=True, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.event.name} - {self.name}'

    
    def save(self, *args, **kwargs):
        if not self.ticket_type_id:
            self.ticket_type_id = 'tty-' + str(uuid.uuid4())[:6]
        super().save(*args, **kwargs)


    class Meta:
        ordering = ('created_at',)


class TicketPurchase(models.Model):
    ticket_id = models.CharField(max_length=15, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateField(auto_now_add=True)
    purchased_at = models.DateTimeField(auto_now_add=True)
    payment_verified = models.BooleanField(default=False)


    def total_amount(self):
        if self.event.is_free:
            return 0
        return self.ticket_type.price * self.quantity

    
    def __str__(self):
        return f'{self.event} - TicketID {self.ticket_id}'

    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = 'tck-' + generate_id(11)
        super().save(*args, **kwargs)

        if self.event.is_free:
            self.ticket_type = None
        super().save(*args, **kwargs)


    
    class Meta:
        ordering = ('-purchased_at', )