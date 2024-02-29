from django.urls import path

from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('', views.index, name='index'),
    path('Admin/',views.login_admin, name ='login_admin'),
    path('Admin/Home/',views.admin_home, name ='admin_home'),
    path('Admin/View/Hotels',views.admin_view_hotel, name= 'admin_view_hotel'),
    path('Admin/Hotel/approve/<int:id>/',views.approve, name='approve'),
    path('Admin/View/Approved/Hotels/',views.approve_view_hotels, name = 'approve_view_hotels'),
    path('Admin/View/Users/',views.admin_view_customers, name='admin_view_customers'),
    path('Admin/logout/', views.admin_logout, name='admin_logout')
]
