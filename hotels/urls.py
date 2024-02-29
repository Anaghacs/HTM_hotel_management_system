from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('Hotel/Signup/', views.hotel_signup, name = 'hotel_signup'),
    path('Hotel/Login', views.hotel_login, name = 'hotel_login'),
    path('Hotel/Dashboard/', views.hotel_dashboard, name = 'hotel_dashboard'),
    path('Hotel/View/Users/', views.hotel_view_customers, name = 'hotel_view_customers'),
    # path('Hotel/Edit/Profile/<int:id>/', views.edit_hotel_details, name = 'edit_hotel_details'),
    # path('Hotel/logout/', views.hotel_logout, name='admin_logout'),


]
