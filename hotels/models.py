from django.db import models

# Create your models here.

class Hotels(models.Model):
      #Create hotel models
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