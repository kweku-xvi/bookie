from .models import Ticket
from django import forms


class Ticket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'event', 'price', 'quantity']