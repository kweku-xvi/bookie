from .forms import TicketTypeForm, BookFreeEventForm, BookPaidEventForm
from .models import TicketType
from .utils import send_booking_confirmation_email, generate_qrcode, upload_to_imgur
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from programs.models import Event
from django.urls import reverse
from django.http import HttpResponse

def add_ticket_view(request, event_id: str): # ADDING A TICKET TYPE 
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


def book_free_events_view(request, event_id:str): # ADD RESTRICTIONS WHEN QUANTITY IS GREATER THAN QUANTITY AVAILABLE
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = BookFreeEventForm(request.POST, initial={'email':request.user.email})

        if form.is_valid():
            ticket_purchase = form.save(commit=False)
            ticket_purchase.event = event
            ticket_purchase.user = request.user
            ticket_purchase.quantity = 1
            ticket_purchase.payment_verified = True
            ticket_purchase.save()

            qr = generate_qrcode(ticket_purchase.ticket_id)
            image_url = upload_to_imgur(qr)

            send_booking_confirmation_email(email=request.user.email, 
                first_name=ticket_purchase.first_name, 
                event_name=event.name,
                ticket_id=ticket_purchase.ticket_id,
                date=str(event.event_date),
                time=str(event.start_time),
                location=event.venue,
                img_url=image_url
                )

            return redirect('booking_confirmation')
    else:
        form = BookFreeEventForm(initial={'email':request.user.email})

    context = {
        'form':form,
        'event':event, 
        'title':f'Book - {event.name}',
    }

    return render(request, 'tickets/book_free_event.html', context)


def book_paid_events_view(request, event_id:str):
    event = get_object_or_404(Event, id=event_id)
    ticket_types = TicketType.objects.filter(event=event)

    if request.method == 'POST':
        form = BookPaidEventForm(request.POST, initial={'email':request.user.email})
        
        if form.is_valid():
            selected_ticket_type_id = request.POST.get('ticket_type')
            selected_ticket_type = TicketType.objects.get(ticket_type_id=selected_ticket_type_id)

            ticket_purchase = form.save(commit=False)
            ticket_purchase.event = event
            ticket_purchase.user = request.user
            ticket_purchase.ticket_type = selected_ticket_type
            ticket_purchase.save()

            selected_ticket_type.quantity_available -= ticket_purchase.quantity
            selected_ticket_type.save()

            qr = generate_qrcode(ticket_purchase.ticket_id)
            image_url = upload_to_imgur(qr)

            send_booking_confirmation_email(email=request.user.email, 
                first_name=ticket_purchase.first_name,
                event_name=event.name,
                ticket_id=ticket_purchase.ticket_id,
                date=str(event.event_date),
                time=str(event.start_time),
                location=event.venue,
                img_url=image_url
                )

            return redirect('booking_confirmation')
    else:
        form = BookPaidEventForm(initial={'email':request.user.email})


    context = {
        'title':f'Book - {event.name}',
        'ticket_types':ticket_types,
        'event':event,
        'form':form
    }

    return render(request, 'tickets/book_paid_event.html', context)


def booking_confirmation_view(request):
    context = {
        'title':'Booking Confirmed',
        'email':request.user.email
    }

    return render(request, 'tickets/booking_confirmation.html', context)


