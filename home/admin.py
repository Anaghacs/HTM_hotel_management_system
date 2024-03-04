from django.contrib import admin

# Register your models here.
from .models import User, Hotel, Customer, Room

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Customer)
admin.site.register(Room)