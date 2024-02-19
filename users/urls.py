from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('user_logins',views.user_logins, name = 'user_logins'),
    path('user_signup',views.user_signup, name ='user_signup'),
    path('user_home',views.user_home, name = 'user_home'),
    path('user_logout',views.user_logout, name = 'user_logout'),
]
