from .models import Event
from django import forms


class EventsForm(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Event
        fields = ['name', 'short_description', 'description', 'category', 'event_date', 'start_time', 'end_time', 'image']