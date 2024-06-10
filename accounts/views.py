from .forms import UserRegistrationForm
from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'accounts/home.html')


def sign_up_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form':form})
