from .forms import EventsForm
from django.shortcuts import render, redirect
from django.urls import reverse


def create_event_view(request):
    if request.method == 'POST':
        form = EventsForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.is_active = False
            event.save()
            return redirect(reverse('add_ticket', args=[event.id]))
    else:
        form = EventsForm()

    context = {
        'title':'Create Event',
        'form':form
    }

    return render(request, 'programs/create_event.html', context)