from . import views
from django.urls import path


urlpatterns = [
    path('create-event/', views.create_event_view, name='create_event'),
    path('<str:event_id>/', views.events_info_view, name='events_info'),
]