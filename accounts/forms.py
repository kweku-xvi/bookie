from .models import User, Profile
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))

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
        fields = ['about', 'phone', 'mobile', 'postal_address', 'website_link', 'twitter_link', 'instagram_link', 'facebook_link', 'image']
        labels = {
            'image':'Change Profile Photo'
        }


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "example.com" in email:
            raise forms.ValidationError("Please use a different email domain.")
        return email


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "example.com" in email:
            raise forms.ValidationError("Please use a different email domain.")
        return email


class CustomUserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_verified:
            raise forms.ValidationError(
                'Your email address is not verified. Please check your email for the verification link.',
                code='unverified',
            )

