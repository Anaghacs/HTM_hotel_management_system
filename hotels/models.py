from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
# Create your models here.



# class Hotels(models.Model):
#       #Create hotel models
#       hotel_name = models.CharField(max_length = 20)      
#       address = models.TextField()
#       place = models.CharField(max_length = 25)
#       email = models.EmailField(max_length = 20)
#       phone = models.CharField(max_length = 12)
#       photo = models.ImageField(upload_to = 'media', blank = True, null = True)

#       user_name = models.CharField(max_length = 25, blank = True, null = True)
#       password = models.CharField(max_length=32, blank = True, null = True)

#       #admin approved field
#       approved = models.BooleanField(default=False)
      
#       #display hotelname
#       def __str__(self):
#             return self.hotel_name
      

# class Users(AbstractUser):
# 	is_admin = models.BooleanField(default=False)
# 	is_patient = models.BooleanField(default=False)
# 	is_doctor = models.BooleanField(default=False)
      
# class CustomHotel(models.Model):
#       hotels = models.ForeignKey(Hotels, on_delete = models.CASCADE)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    hotel_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    hotel_id   = models.CharField(max_length=20, unique=True)
    place = models.CharField(max_length = 25)
    district = models.CharField(max_length = 150)
    state = models.CharField(max_length = 40)

    profile_photo = models.ImageField(upload_to='images/profile_photos', null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    created_date  = models.DateTimeField(auto_now_add=True)
    approval_status   = models.CharField(default="New Request", max_length=50)
    objects = CustomUserManager()
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    class Meta:
        verbose_name_plural = 'HOTEL_Management'


      