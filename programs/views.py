from .forms import EventsForm, EditEventInfoForm
from .models import Event
from accounts.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from tickets.models import TicketPurchase, TicketType


def create_event_view(request):
    if request.method == 'POST':
        form = EventsForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.is_active = False
            event.organized_by = request.user

            if event.is_free:
                event.is_active = True
                event.save()
                messages.success(request, f'Your event has been successfully created!')
                return redirect(reverse('events_info', args=[event.id]))

            event.save()
            return redirect(reverse('add_ticket', args=[event.id]))
    else:
        form = EventsForm()

    context = {
        'title':'Create Event',
        'form':form
    }

    return render(request, 'programs/create_event.html', context)


def update_event_view(request, event_id:str):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        form = EditEventInfoForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            event.save()

            messages.success(request, f'Your event has been successfully updated!')
            return redirect(reverse('events_info', args=[event.id]))
    else:
        form = EditEventInfoForm(instance=event)

    context = {
        'form':form, 
        'event':event,
        'title':f'Update - {event.name}'
    }

    return render(request, 'programs/update_event.html', context)


def events_info_view(request, event_id:str):
    if Event.objects.filter(id=event_id).exists:
        event = Event.objects.get(id=event_id)
    else:
        return HttpResponse('<h1>Event does not exist</h1>')

    context = {
        'title':event.name,
        'event':event,
        'organizer':event.organized_by,
        'ticket_types':TicketType.objects.filter(event=event)
    }

    return render(request, 'programs/events_info.html', context)


def organizer_profile_view(request, id:str):
    organizer = User.objects.get(id=id)

    context = {
        'title':organizer.username,
        'organizer':organizer,
    }

    return render(request, 'programs/organizer_profile.html', context)


def events_organized_by_user_view(request, id:str):
    organizer = User.objects.get(id=id)
    events = Event.objects.filter(is_active=True, organized_by=organizer)

    paginator = Paginator(events, 4)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    context = {
        'title':f"Events - {organizer.first_name} {organizer.last_name}",
        'events':events,
        'organizer':organizer
    }

    return render(request, 'programs/organized_events.html', context)


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


def event_dashboard_view(request, event_id:str):
    event = get_object_or_404(Event, id=event_id)
    tickets_sold = TicketPurchase.objects.filter(event=event, payment_verified=True)
    total_orders = tickets_sold.count()

    paginator = Paginator(tickets_sold, 10)
    page_number = request.GET.get('page')
    tickets_sold = paginator.get_page(page_number)

    total_revenue = 0
    ticket_quantity = 0
    for ticket in tickets_sold:
        total_revenue += ticket.total_amount()
        ticket_quantity += ticket.quantity

    context = {
        'title':f'Dashboard - {event.name}',
        'event':event,
        'tickets':tickets_sold,
        'tickets_sold':ticket_quantity,
        'revenue':total_revenue,
        'total_orders':total_orders,
    }

    return render(request, 'programs/event_dashboard.html', context)


def event_tickets_info_view(request, event_id:str):
    event = get_object_or_404(Event, id=event_id)

    context = {
        'title':f'Tickets - {event.name}',
        'event':event,
        'ticket_types':TicketType.objects.filter(event=event)
    }

    return render(request, 'programs/event_tickets_info.html', context)
