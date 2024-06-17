from .forms import EventsForm
from django.shortcuts import render, redirect


def create_event_view(request):
    if request.method == 'POST':
        form = EventsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventsForm()

    context = {
        'title':'Create Event',
        'form':form
    }

    return render(request, 'programs/create_event.html', context)