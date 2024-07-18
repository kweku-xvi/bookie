from . import views
from django.urls import path

urlpatterns = [
    path('checkout/<str:ticket_id>/', views.checkout, name='checkout'),
]