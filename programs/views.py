from .forms import EventsForm
from .models import Event
from accounts.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def create_event_view(request):
    if request.method == 'POST':
        form = EventsForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.is_active = False
            event.organized_by = request.user
            event.save()
            return redirect(reverse('add_ticket', args=[event.id]))
    else:
        form = EventsForm()

    context = {
        'title':'Create Event',
        'form':form
    }

    return render(request, 'programs/create_event.html', context)


def events_info_view(request, event_id:str):
    if Event.objects.filter(id=event_id).exists:
        event = Event.objects.get(id=event_id)
    else:
        return HttpResponse('<h1>Event does not exist</h1>')

    context = {
        'title':event.name,
        'event':event
    }

    return render(request, 'programs/events_info.html', context)


def organizer_profile_view(request, id:str):
    user = User.objects.get(id=id)

    context = {
        'title':user.username,
        'user':user
    }

    return render(request, 'programs/organizer_profile.html', context)


def search_events_view(request):
    query = request.GET.get('search', '')
    results = []

    if query:
        results = Event.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(venue__icontains=query) |
            Q(category__icontains=query)
        )

    paginator = Paginator(results, 8)

    page_number = request.GET.get('page')
    results = paginator.get_page(page_number)


    context = {
        'title':'Search',
        'query':query,
        'results':results,
    }

    return render(request, 'programs/search.html', context)