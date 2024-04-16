from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid 
uuid.uuid4()
from django.utils.translation import gettext_lazy as _
# from .constants import PaymentStatus
from django.db.models.fields import CharField

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "CUSTOMER"
        HOTEL = "HOTEL", "HOTEL"

    base_role = Role.ADMIN

    role = models.CharField(max_length = 50, choices = Role.choices)


class Customer(User):
    base_role = User.Role.CUSTOMER
    address = models.CharField(blank = True, max_length = 100)
    
    place = models.CharField(blank = True, max_length = 20)
    emails = models.EmailField(max_length = 100, unique = True)
    phone = models.CharField(max_length = 12, unique = True)
    is_deleted = models.BooleanField(default = False)


    class Meta:
        verbose_name = "Customer user"

    def welcome(self):
        return "Only for users"


class Hotel(User):
    base_role = User.Role.HOTEL
    hotel_name = models.CharField(max_length = 20)      
    address = models.CharField(blank = True, max_length = 100)
    place = models.CharField(blank = True, max_length = 20)
    emails = models.EmailField(max_length = 100, unique = True)
    phone = models.CharField(max_length = 12, unique = True)
    photo = models.ImageField(upload_to = 'media', blank = True, null = True)
    approved = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)

    hotel_number = models.IntegerField(null=True,blank=True)
    class Meta:
        verbose_name = "Hotel User"


    def welcome(self):
        return "Only for Hotels"


class Room(models.Model):
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),

    )

    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    room_number = models.IntegerField(primary_key=True)
    capacity = models.SmallIntegerField()
    number_of_beds = models.SmallIntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.CharField(max_length=7,null=True,blank=True)

    floor_number = models.IntegerField()
    photo = models.ImageField(upload_to = 'media', blank = True, null = True)
    is_deleted = models.BooleanField(default = False)


    def __str__(self):
        return str(self.room_number)
    
    
class Facilities(models.Model):

    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    facility = models.CharField(max_length = 20)      
    description = models.TextField(max_length = 20, blank = True )
    photo = models.ImageField(upload_to = 'media', blank = True, null = True)
    is_deleted = models.BooleanField(default = False)

    def __str__(self):
        return str(self.facility)
    
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    guest_number = models.IntegerField()
    paid_amount = models.BooleanField(default=False)
    cost = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return f"Booking for {self.customer} Hotel : {self.room.hotel} - Room Type : {self.room.room_type} and Room Number : {self.room.room_number}"


class Order(models.Model):
    
    customer = models.CharField(max_length=40,null=True,blank=True)
    email_id =models.CharField(max_length=150,null=True,blank=True)
    room_id = models.IntegerField()
    finder = models.CharField(max_length=150,null=True,blank=True)
    razorpay_order_id = models.CharField(max_length=60)
    signature_id = models.CharField(max_length=128, null=False, blank=False)
    amount = models.CharField(max_length=7,null=True,blank=True)
    paid_amount = models.BooleanField(default=False)
    status = models.CharField(max_length=20,blank=True)
    hotel = models.CharField(max_length=50,null=True,blank=True)
    boock_date = models.DateTimeField(auto_now_add=True)
    reason=models.CharField(max_length=250,null=True,blank=True)
    code=models.CharField(max_length=250,null=True,blank=True)
    source=models.CharField(max_length=250,null=True,blank=True)
    step=models.CharField(max_length=250,null=True,blank=True) 


    def _str_(self):
            return f"{self.customer}  {self.email_id}  {self.status}  {self.amount}  {self.room_id}  {self.order_id}  {self.signature_id}  {self.ordered_date} {self.razorpay_order_id} {self.reason} {self.code} {self.source} {self.step} {self.payment_id} "
    
# class PaymentFailed(models.Model): 
#       order_id=models.CharField(max_length=250)
#       reason=models.CharField(max_length=250)

#       code=models.CharField(max_length=250)

#       source=models.CharField(max_length=250)

#       step=models.CharField(max_length=250)

#       payment_id=models.CharField(max_length=250)

#       date_time=models.DateTimeField(auto_now_add=True)

#   
#     def _str_(self):
#             return f"{self.order_id} {self.reason} {self.code} {self.source} {self.step} {self.payment_id} {self.date_time}"
      

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.CUSTOMER:
            Customer.objects.create(user=instance)
        elif instance.role == User.Role.HOTEL:
            Hotel.objects.create(user=instance)

