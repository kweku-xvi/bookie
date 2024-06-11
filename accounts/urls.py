from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up_view, name='signup'),
    path('verify-user/', views.verify_user_view, name='verify_user'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]