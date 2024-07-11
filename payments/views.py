from .models import Payment
from .utils import initialize_transaction, generate_id
from accounts.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from tickets.models import TicketPurchase


def checkout(request, ticket_id:str):
    email = request.user.email
    ticket_purchase = get_object_or_404(TicketPurchase, ticket_id=ticket_id)

    transaction = initialize_transaction(email=email, amount=str(ticket_purchase.total_amount() * 100), reference=ticket_id)

    context = {
        'transaction':transaction,
    }

    return render(request, 'tickets/confirm_payment.html', context)
