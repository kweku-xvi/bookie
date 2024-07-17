from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up_view, name='signup'),
    path('verify-user/', views.verify_user_view, name='verify_user'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('filter/category/<str:category>/', views.filter_events_by_category, name='filter_events_by_category'),
    path('filter/date/<str:date_filter>/', views.filter_events_by_date_view, name='filter_events_by_date'),
    path('filter/category/<str:category>/date/<str:date_filter>/', views.filter_event_by_category_and_date, name='filter_events_by_category_and_date'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('faq/', views.faq_view, name='faq'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('contact-us/sent/', views.feedback_sent_view, name='feedback_sent'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-done/',PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
]
