from django.contrib import admin

# Register your models here.
from soulFoodApp.models import Shop, Item, Order, OrderDetail, Customer

admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Customer)
