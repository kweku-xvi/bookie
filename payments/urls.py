from . import views
from django.urls import path


urlpatterns = [
    path('<str:ticket_id>/', views.buy_tickets, name='checkout'),
]