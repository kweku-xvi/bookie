import os, jwt
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import User
from .utils import send_mail_verification
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from dotenv import load_dotenv
from programs.models import Event


load_dotenv()


def home(request):
    events_list = Event.objects.all()
    paginator = Paginator(events_list, 8)

    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    context = {
        'events':events, 
        'title':'Home'
    }
    return render(request, 'accounts/home.html', context)


def sign_up_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            user = User.objects.get(email=form.cleaned_data['email'])
            token = jwt.encode({'user_id':user.id}, os.getenv('SECRET_KEY'), algorithm='HS256')
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_user')
            absolute_url = f'http://{current_site}{relative_link}?token={token}'
            link = str(absolute_url)
            send_mail_verification(username=user.username, email=user.email, link=link)

            messages.success(request, f'Your account has been created! Please verify your email and log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form':form})


def verify_user_view(request):
    token = request.GET.get('token')

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])

        if not user.is_verified:
            user.is_verified = True
            user.save()

            return HttpResponse('<h1>Email verified successfully</h1>')
        else:
            return HttpResponse('<h1>Email already verified</h1>')
    except jwt.ExpiredSignatureError:
        return HttpResponse('<h1>Activation link expired</h1>')
    except jwt.DecodeError:
        return HttpResponse('<h1>Invalid token</h1>')
    except jwt.InvalidTokenError:
        return HttpResponse('<h1>Invalid token</h1>')
    except User.DoesNotExist:
        return HttpResponse('<h1>User does not exist</h1>')
    except Exception as e:
        return HttpResponse(f'<h1>Error: {str(e)}</h1>')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'title':'Profile',
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'accounts/profile.html', context)