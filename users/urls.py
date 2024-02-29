from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('User/Signup/',views.user_signup, name = "user_signup"),
    path('User/Login/',views.user_login, name = "user_login"),
    path('User/Home/',views.user_home, name = "user_home"),
    path('User/Logout/', views.user_logout, name = "user_logout"),
]
