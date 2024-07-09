from .models import TicketType, TicketPurchase
from django import forms


class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'quantity_available']


class BookFreeEventForm(forms.ModelForm):
    class Meta:
        model = TicketPurchase
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True  
        