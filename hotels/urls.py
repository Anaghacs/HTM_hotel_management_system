from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('Hotel/Signup/', views.hotel_signup, name='hotel_signup'),
    path('Hotel/Login',views.hotel_login, name = 'hotel_login'),
    path('Hotel/Dashboard/',views.hotel_dashboard, name = 'hotel_dashboard'),
]
