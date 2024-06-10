from .models import User
from django import forms
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, max_length=100, widget=forms.PasswordInput)

    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Username is already in use.')
        
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email is already in use.')
        
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user
        