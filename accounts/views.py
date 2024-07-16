import os, jwt
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, ContactUsForm
from .models import User
from .utils import send_mail_verification, contact_us_mail, contact_us_mail_response
from datetime import datetime, timedelta
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now
from dotenv import load_dotenv
from programs.models import Event


load_dotenv()


@login_required
def home(request):
    events_list = Event.objects.filter(is_active=True)
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
def update_profile(request):
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
        'title':'Update Profile',
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'accounts/update_profile.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
    

def filter_events_by_date_view(request, date_filter:str):
    today = now().date()
    events = Event.objects.filter(is_active=True)

    if date_filter == 'today':
        events = events.filter(event_date=today)
    elif date_filter == 'tomorrow':
        tomorrow = today + timedelta(days=1)
        events = events.filter(event_date=tomorrow)
    elif date_filter == 'next_week':
        next_week = today + timedelta(days=7)
        events = events.filter(event_date__gte=today, event_date__lte=next_week)
    elif date_filter == 'next_month':
        next_month = today + timedelta(days=30)
        events = events.filter(event_date__gte=today, event_date__lte=next_month)
    elif date_filter == 'this_year':
        end_of_year = datetime(today.year, 12, 31).date()
        events = events.filter(event_date__gte=today, event_date__lte=end_of_year)

    paginator = Paginator(events, 8)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    context = {
        'title':'Home',
        'events':events,
        'date_filter':date_filter
    }

    return render(request, 'accounts/filter_events_by_date.html', context)


def filter_events_by_category(request, category:str):
    events = Event.objects.filter(is_active=True)

    if category == 'arts':
        events = events.filter(category='arts')
    elif category == 'business':
        events = events.filter(category='business')
    elif category == 'concert':
        events = events.filter(category='concert')
    elif category == 'education':
        events = events.filter(category='education')
    elif category == 'fashion':
        events = events.filter(category='fashion')
    elif category == 'film':
        events = events.filter(category='film')
    elif category == 'health':
        events = events.filter(category='health')
    elif category == 'music':
        events = events.filter(category='music')
    elif category == 'politics':
        events = events.filter(category='politics')
    elif category == 'scienceandtechnology':
        events = events.filter(category='scienceandtechnology')
    elif category == 'others':
        events = events.filter(category='others')


    paginator = Paginator(events, 8)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    context = {
        'events':events, 
        'title':'Home',
        'category':category,
    }
    
    return render(request, 'accounts/filter_events_by_category.html', context)


def filter_event_by_category_and_date(request, category:str, date_filter:str):
    today = now().date()

    category_map = {
        'arts': 'arts',
        'business': 'business',
        'concert': 'concert',
        'education': 'education',
        'fashion': 'fashion',
        'film': 'film',
        'health':'health',
        'music': 'music',
        'politics': 'politics',
        'scienceandtechnology': 'scienceandtechnology',
        'others': 'others'
    }

    date_filter_map = {
        'today':'today',
        'tomorrow':'tomorrow',
        'next_week':'next_week',
        'next_month':'next_month',
        'this_year':'this_year',
    }

    if not category in category_map or not date_filter in date_filter_map:
        return render(request, '404.html', status=404)

    events = Event.objects.filter(is_active=True, category=category_map[category])

    if date_filter == 'today':
        events = events.filter(event_date=today)
    elif date_filter == 'tomorrow':
        tomorrow = today + timedelta(days=1)
        events = events.filter(event_date=tomorrow)
    elif date_filter == 'next_week':
        next_week = today + timedelta(days=7)
        events = events.filter(event_date__gte=today, event_date__lte=next_week)
    elif date_filter == 'next_month':
        next_month = today + timedelta(days=30)
        events = events.filter(event_date__gte=today, event_date__lte=next_month)
    elif date_filter == 'this_year':
        end_of_year = datetime(today.year, 12, 31).date()
        events = events.filter(event_date__gte=today, event_date__lte=end_of_year)

    paginator = Paginator(events, 8)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    context = {
        'events':events, 
        'title':'Home',
        'category':category,
        'date_filter':date_filter,
    }

    return render(request, 'accounts/filter_events_by_category_and_date.html', context)


def custom_404(request, exception):
    return render(request, 'accounts/404.html', status=404)


def custom_500(request):
    return render(request, 'accounts/500.html', status=500)


def about_us_view(request):
    return render(request, 'accounts/about_us.html', {'title':'About Us'})


def faq_view(request):
    return render(request, 'accounts/faq.html', {'title':'FAQ'})


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            contact_us_mail(
                name=name,
                subject=subject,
                senders_email=email,
                message=message
            )

            contact_us_mail_response(
                email=email,
                name=name
            )

            return redirect('feedback_sent')
    else:
        form = ContactUsForm()

    context = {
        'title':'Contact Us',
        'form':form
    }

    return render(request, 'accounts/contact_us.html', context)


def feedback_sent_view(request):
    return render(request, 'accounts/feedback_sent.html', {'title':'Message Sent'})