from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class Customuser(AbstractUser):
#       user_type = ((1,"Hotels"),)
#       user_type = models.CharField(default = 1, choices = user_type, max_length = 10 )

class Hotels(models.Model):
      #Create hotel models
      # admin = models.OneToOneField(Customuser, on_delete = models.CASCADE, blank = True, null = True)
      hotel_name = models.CharField(max_length = 20)      
      address = models.TextField()
      place = models.CharField(max_length = 25)
      email = models.EmailField(max_length = 20)
      phone = models.CharField(max_length = 12)
      photo = models.ImageField(upload_to = 'media', blank = True, null = True)

      user_name = models.CharField(max_length = 25, blank = True, null = True)
      password = models.CharField(max_length=32, blank = True, null = True)

      #admin approved field
      approved = models.BooleanField(default=False)
      
      #display hotelname
      def __str__(self):
            return self.hotel_name