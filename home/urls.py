from django.urls import path

from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('', views.index, name='index'),
    path('Admin/Login',views.admin_login, name = 'admin_login'),
    path('Admin/Home/',views.admin_home, name = 'admin_home'),
    

    

]
