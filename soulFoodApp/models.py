from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

        
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


class Order(models.Model):
    ORDERED = 1
    SHIPPED = 2
    OUT_FOR_DELIVERY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (ORDERED, "Ordered"),
        (SHIPPED, "Shipped"),
        (OUT_FOR_DELIVERY, "Out for delivery"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer)
    shop = models.ForeignKey(Shop)

    address = models.CharField(max_length=500)
    total = models.FloatField()
    status = models.IntegerField(choices = STATUS_CHOICES)

    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name="order_details")

    item = models.ForeignKey(Item)
    qty = models.IntegerField()
    sub_total = models.FloatField()


    def __str__(self):
        return str(self.id)