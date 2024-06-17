from .models import Ticket
from django import forms


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'price', 'quantity']