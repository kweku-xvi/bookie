from . import views
from django.urls import path


urlpatterns = [
    path('<str:event_id>/', views.add_ticket_view, name='add_ticket'),
]