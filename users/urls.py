from django.urls import path
from . import views

urlpatterns = [
    # Add more URL patterns as needed
#     path('signup',views.signup, name ='signup'),
    path('user_home',views.user_home, name = 'user_home')
]
