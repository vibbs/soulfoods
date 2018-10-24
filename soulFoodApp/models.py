from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='shop_logo/', blank=False)

    #the below is needed so that the view on the admin page is redable
    def __str__(self):
        return self.name
