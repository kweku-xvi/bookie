from accounts.models import User
from django.db import models
from tickets.models import TicketPurchase


class Payment(models.Model):
    payment_id = models.CharField(max_length=20, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_purchased = models.OneToOneField(TicketPurchase, on_delete=models.CASCADE)
    paid_at = models.DateTimeField()


    def __str__(self):
        return f'Payment: {self.payment_id}, By: {self.user.username}, Amount: {self.amount} '

    
    class Meta:
        ordering = ('paid_at',)