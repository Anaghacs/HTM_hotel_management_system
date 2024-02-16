from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('', views.index, name='index'),
    path('signup',views.signup, name='signup'),
    # path('hotel_signup',views.hotel_signup, name='hotel_signup'),
    path('logins',views.logins, name='logins'),
]
