from . import views
from django.urls import path


urlpatterns = [
    path('<str:event_id>/add/', views.add_ticket_view, name='add_ticket'),
    path('event/<str:event_id>/book/free/', views.book_free_events_view, name='book_free_event'),
    path('event/<str:event_id>/book/', views.book_paid_events_view, name='book_paid_event'),
    path('booking-confirmed/', views.booking_confirmation_view, name='booking_confirmation'),
    path('payment-confirmation/<str:ticket_id>/', views.payment_confirmation_view, name='payment_confirmation'),
    path('type/<str:ticket_type_id>/update/', views.update_ticket_type_view, name='update_ticket_type'),
    path('quantity-error/', views.quantity_error_page_view, name='quantity_error'),
    path('<str:ticket_id>/invoice/', views.invoice_view, name='invoice'),
]