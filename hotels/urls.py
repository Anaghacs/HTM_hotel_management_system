from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('hotel_signup',views.hotel_signup, name ='hotel_signup'),
    path('hotel_home',views.hotel_home, name = 'hotel_home'),
    path('hotel_login',views.hotel_login, name='hotel_login'),
]
