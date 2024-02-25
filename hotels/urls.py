from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    # path("Hotel/SignUp/",views.hotel_signup, name = "hotel_signup"),
    # path("Hotel/Signup/",views.hotel_signup, name= "hotel_signup"),
    path('hotel/signup/', views.hotel_signup, name='hotel_signup'),
]
