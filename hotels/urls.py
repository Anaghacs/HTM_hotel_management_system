from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('Hotel/Signup/', views.hotel_signup, name = 'hotel_signup'),
    path('Hotel/Login/', views.hotel_login, name = 'hotel_login'),
    path('logout/', views.logout, name = 'logout'),

    path('Hotel/Dashboard', views.hotel_dashboard, name = 'hotel_dashboard'),
    path('Hotel/Rooms/', views.add_hotel_room, name = 'add_hotel_room'),
    path('Hotel/View/Rooms/', views.hotels_view_room_details, name= 'hotels_view_room_details'),
    path('Hotel/Delete/Room/<int:room_number>/', views.delete_room, name = 'delete_room'),
    path('Hotel/Room/update/<int:room_number>/', views.update_room_details, name = 'update_room_details'),
    path('Hotel/Update/Room/<int:room_number>/', views.update_rooms, name = 'update_rooms'),

    path('Hotel/Add/Facilities/', views.add_hotel_facilities, name = 'add_hotel_facilities'),
    path('Hotel/View/Facilities/', views.hotel_view_facilities, name = 'hotel_view_facilities'),
    path('Hotel/Delete/Facilities/<int:id>/', views.hotel_delete_facilities, name = 'hotel_delete_facilities'),
    path('Hotel/Update/Facilities/<int:id>/', views.hotel_update_facilities, name = 'hotel_update_facilities'),
    path('Hotel/Update/Facilitity/<int:id>/', views.update_facilities, name = 'update_facilities'),

    path('Hotel/Avilable/Rooms', views.room_availability, name = "room_availability"),


]
