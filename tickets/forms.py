from .models import TicketType, TicketPurchase
from django import forms


class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'quantity_available']

        labels = {
            'price':'Price (GHC)'
        }


class UpdateTicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'quantity_available']

        labels = {
            'price':'Price (GHC)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True


class BookFreeEventForm(forms.ModelForm):
    class Meta:
        model = TicketPurchase
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True  


class BookPaidEventForm(forms.ModelForm):
    class Meta:
        model = TicketPurchase
        fields = ['first_name', 'last_name', 'quantity', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True  
