from .forms import TicketTypeForm
from .models import TicketType
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from programs.models import Event
from django.urls import reverse

def add_ticket_view(request, event_id: str):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = TicketTypeForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.event = event

            if TicketType.objects.filter(name=form.cleaned_data['name'], event=event):
                    messages.error(request, f'Ticket with this name already exists')
                    return redirect(reverse('add_ticket', args=[event.id]))
                    
            if 'save' in request.POST:
                ticket.save()
                
                event.is_active = True
                event.save()

                messages.success(request, f'Ticket type saved successfully')
                return redirect('home')

            elif 'save_add_another' in request.POST:
                ticket.save()

                event.is_active = True
                event.save()

                messages.success(request, f'Ticket saved! You can add another')
                return redirect(reverse('add_ticket', args=[event.id]))
    else:
        form = TicketTypeForm()

    context = {
        'form': form,
        'title': 'Tickets'
    }

    return render(request, 'tickets/add_ticket.html', context)
