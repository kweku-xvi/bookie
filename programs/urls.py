from . import views
from django.urls import path


urlpatterns = [
    path('create-event/', views.create_event_view, name='create_event'),
    path('organizer/<str:id>/', views.organizer_profile_view, name='event_organizer'),
    path('organizer/<str:id>/all-events/', views.events_organized_by_user_view, name='event_organized_by_user'),
    path('search/', views.search_events_view, name='search'),
    path('<str:event_id>/', views.events_info_view, name='events_info'),
    path('<str:event_id>/update/', views.update_event_view, name='update_event'),
    path('<str:event_id>/dashboard/', views.event_dashboard_view, name='event_dashboard'),
]