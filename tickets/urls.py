from . import views
from django.urls import path


urlpatterns = [
    path('<str:event_id>/add/', views.add_ticket_view, name='add_ticket'),
    path('event/<str:event_id>/book/', views.book_free_events_view, name='book_free_event'),
    path('booking-confirmed/', views.booking_confirmation_view, name='booking_confirmation'),
]