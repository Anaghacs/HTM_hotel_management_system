from django.urls import path

from . import views

urlpatterns = [
    # Add more URL patterns as needed
    path('', views.index, name='index'),
    # path('signup',views.signup, name='signup'),
    path('logins',views.logins, name='logins'),
    path('admin_home',views.admin_home, name='admin_home'),
    path('admin_view_hotels',views.admin_view_hotels, name='admin_view_hotels'),
    path('admin_view_users',views.admin_view_users, name='admin_view_users'),
    path('approve/<int:id>/',views.approve, name='approve'),

]
