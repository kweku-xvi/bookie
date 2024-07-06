from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up_view, name='signup'),
    path('verify-user/', views.verify_user_view, name='verify_user'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('category/<str:category>/', views.filter_events_by_category, name='filter_events_by_category'),
    path('date/<str:date_filter>/', views.filter_events_by_date_view, name='filter_events_by_date'),
]
