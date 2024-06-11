from .models import User, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']