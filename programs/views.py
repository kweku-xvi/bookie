from .forms import EventsForm
from .models import Event
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
    event = Event.objects.get(id=event_id)

    context = {
        'title':event.name,
        'event':event
    }

    return render(request, 'programs/events_info.html', context)