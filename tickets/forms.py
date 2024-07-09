from .models import TicketType
from django import forms


class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'quantity_available']