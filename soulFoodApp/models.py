from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    shop_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='shop_logo/', blank=False)

    #the below is needed so that the view on the admin page is redable
    def __str__(self):
        return self.shop_name


class Item(models.Model):
    shop = models.ForeignKey(Shop)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='shop_logo/', blank=True)
    price = models.IntegerField(default=0)
    quantity_per_package = models.CharField(max_length=500)
    is_veg = models.BooleanField(default=False)
    is_soldout = models.BooleanField(default=False)

    def __str__(self):
        return self.name
