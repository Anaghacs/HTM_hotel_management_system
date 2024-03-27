from django.db import models

# Create your models here.
class Storedotps(models.Model):
    email_id=models.EmailField()
    # phone_number=models.IntegerField()
    otp=models.CharField(max_length=6)
    is_active=models.BooleanField(default=True)
    valid_from=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_id