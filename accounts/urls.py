from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('arts/', views.filter_home_by_art_events_view, name='filter_events_by_arts'),
    path('business/', views.filter_home_by_business_events_view, name='filter_events_by_business'),
    path('concert/', views.filter_home_by_concert_events_view, name='filter_events_by_concert'),
    path('education/', views.filter_home_by_education_events_view, name='filter_events_by_education'),
    path('fashion/', views.filter_home_by_fashion_events_view, name='filter_events_by_fashion'),
    path('film/', views.filter_home_by_film_events_view, name='filter_events_by_film'),
    path('music/', views.filter_home_by_music_events_view, name='filter_events_by_music'),
    path('politics/', views.filter_home_by_politics_events_view, name='filter_events_by_politics'),
    path('science/', views.filter_home_by_science_events_view, name='filter_events_by_science'),
    path('others/', views.filter_home_by_others_events_view, name='filter_events_by_others'),
    path('signup/', views.sign_up_view, name='signup'),
    path('verify-user/', views.verify_user_view, name='verify_user'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]