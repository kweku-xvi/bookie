from . import views
from django.urls import path


urlpatterns = [
    path('create-event/', views.create_event_view, name='create_event'),
]