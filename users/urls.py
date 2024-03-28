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
    path('User/Room/Booking/', views.booking_confirmation, name = "booking_confirmation"),

    path('User/Booking/Confirmation/download/', views.booking_details_pdf, name = "booking_details_pdf"),
    path('confirmation/<int:id>/', views.confirmation, name = "confirmation"),
#     path("callback/", views.callback, name = "callback"),
    path('success/',views.paymentsuccess,name="success"),
    # path('failed/',views.paymentfaild,name="failed"),
    path('generate_and_send_otp/', views.generate_and_send_otp, name='generate_and_send_otp'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('handle_otp/',views.validate_otp,name='validate_otp'),

    path('Room/Booking/Details/', views.room_reservation_details, name = "room_reservation_details"),

]
