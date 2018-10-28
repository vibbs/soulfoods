from rest_framework import serializers

from soulFoodApp.models import Shop, Item


class ShopSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, shop):
        request = self.context.get('request')
        logo_url = shop.logo.url 
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Shop
        fields = ("id", "shop_name", "phone", "address", "logo")


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, item):
        if item.image == "":
            return "" #TODO: can add a basic default image if need be
        request = self.context.get('request')
        image_url = item.image.url 
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Item
        fields = ("id", "name", "description", "image", "price", "quantity_per_package", "is_veg", "is_soldout")