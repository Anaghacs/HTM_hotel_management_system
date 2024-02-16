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
      
      #display hotelname
      def __str__(self):
            return self.hotel_name