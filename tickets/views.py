import json
from .forms import TicketTypeForm, BookFreeEventForm, BookPaidEventForm, UpdateTicketTypeForm
from .models import TicketType, TicketPurchase
from .utils import send_booking_confirmation_email, generate_qrcode, upload_to_imgur
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from programs.models import Event
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from payments.models import Payment
from payments.utils import verify_payment
from payments.views import checkout
from urllib.parse import urlparse


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
                return redirect(reverse('events_info', args=[event.id]))
                

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

            return checkout(request, ticket_purchase.ticket_id)
    else:
        form = BookPaidEventForm(initial={'email':request.user.email})


    context = {
        'title':f'Book - {event.name}',
        'ticket_types':ticket_types,
        'event':event,
        'form':form
    }

    return render(request, 'tickets/book_paid_event.html', context)


def payment_confirmation_view(request, ticket_id:str): #Not working
    ticket_purchase = get_object_or_404(TicketPurchase, ticket_id=ticket_id)


    payment_successful = verify_payment(ticket_id)
    print(payment_successful)

    if payment_successful:
        qr = generate_qrcode(ticket_purchase.ticket_id)
        image_url = upload_to_imgur(qr)

        send_booking_confirmation_email(email=request.user.email, 
            first_name=ticket_purchase.first_name,
            event_name=ticket_purchase.event.name,
            ticket_id=ticket_purchase.ticket_id,
            date=str(ticket_purchase.event.event_date),
            time=str(ticket_purchase.event.start_time),
            location=ticket_purchase.event.venue,
            img_url=image_url
        )

        Payment.objects.create(
            payment_id='pay-' + ticket_id,
            user=request.user,
            amount=ticket_purchase.total_amount(),
            ticket_purchased=ticket_purchase,
            paid_at=timezone.now()
        )

        ticket_purchase.payment_verified = True
        ticket_purchase.ticket_type.quantity_available -= ticket_purchase.quantity
        ticket_purchase.ticket_type.save()
        ticket_purchase.save()

        return redirect('booking_confirmation')
    else:
        return HttpResponse('<h1>Payment Failed. Please try again.</h1>')


def booking_confirmation_view(request):
    context = {
        'title':'Booking Confirmed',
        'email':request.user.email
    }

    return render(request, 'tickets/booking_confirmation.html', context)


def update_ticket_type_view(request, ticket_type_id:str):
    ticket_type = get_object_or_404(TicketType, ticket_type_id=ticket_type_id)
    event = ticket_type.event

    if request.method == 'POST':
        form = UpdateTicketTypeForm(request.POST, instance=ticket_type)

        if form.is_valid():
            form.save()

            return redirect(reverse('event_tickets_info', args=[ticket_type.event.id]))
    else:
        form = UpdateTicketTypeForm(instance=ticket_type)

    context = {
        'title':f'Update - {ticket_type.name}',
        'form':form,
        'ticket_type':ticket_type
    }

    return render(request, 'tickets/update_ticket_type.html', context)