from . import views
from django.urls import path


urlpatterns = [
    path('<str:ticket_id>/', views.checkout, name='checkout'),
]