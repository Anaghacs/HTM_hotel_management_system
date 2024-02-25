from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "CUSTOMER"
        HOTEL = "HOTEL", "HOTEL"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)


    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.base_role
    #     return super().save(*args, **kwargs)


# class CustomerManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.CUSTOMER)

class Customer(User):
    base_role = User.Role.CUSTOMER
    address = models.CharField(blank=True, max_length=100)
    place = models.CharField(blank=True, max_length=20)
    district = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    emails = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length = 12, unique = True)

    # student = CustomerManager()

    class Meta:
        verbose_name = "Customer user"

    def welcome(self):
        return "Only for users"

# class HotelManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.HOTEL)

class Hotel(User):
    base_role = User.Role.HOTEL
    hotel_name = models.CharField(max_length = 20)      
    address = models.CharField(blank=True, max_length=100)
    place = models.CharField(blank=True, max_length=20)
    district = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    emails = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length = 12, unique = True)
    photo = models.ImageField(upload_to = 'media', blank = True, null = True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Hotel User"

    # model methods
    # def approve(self):
    #     self.approved = True
    #     return self.save()
    
    # student = HotelManager()

    def welcome(self):
        return "Only for Hotels"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.CUSTOMER:
            Customer.objects.create(user=instance)
        elif instance.role == User.Role.HOTEL:
            Hotel.objects.create(user=instance)

