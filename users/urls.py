from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('User/Signup/', views.user_signup, name = "user_signup"),
    path('User/Login/', views.user_login, name = "user_login"),
    path('User/Home/', views.user_home, name = "user_home"),
    path('User/Logout/', views.user_logout, name = "user_logout"),
    path('User/Room/View/<int:id>/', views.room_list, name = "room_list"),
    path('User/Room/Reservation/<int:room_number>/', views.room_reservation, name = "room_reservation"),
    path('User/Check/Availability/<int:room_number>/', views.check_room_availability, name = "check_room_availability"),
    path('User/Room/Booking/<int:room_number>/', views.room_booking, name = "room_booking"),
    path('User/Booking/Confirmation/', views.booking_confirmation, name = "booking_confirmation"),
    path('confirmation/<int:id>/', views.confirmation, name = "confirmation"),
    # path("payment/", views.order_payment, name = "payment"),
#     path("callback/", views.callback, name = "callback"),

    path('success/',views.paymentsuccess,name="success"),
    # path('failed/',views.paymentfaild,name="failed"),
]
 