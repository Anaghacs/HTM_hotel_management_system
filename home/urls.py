from django.urls import path

from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('', views.index, name='index'),
    path('Admin/Logins/',views.login_admin, name ='login_admin'),
    path('Admin/Home/',views.admin_home, name ='admin_home'),
    path('Admin/View/Hotels',views.admin_view_hotel, name= 'admin_view_hotel'),
    path('Admin/Hotel/approve/<int:id>/',views.approve, name='approve'),


]
