import json
from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from soulFoodApp.models import Shop, Item, Order, OrderDetail
from soulFoodApp.serializers import ShopSerializer, ItemSerializer, OrderSerializer

# from oauth2_provider.oauth2_validators import OAuth2Validator as \
#     OrigOAuth2Validator


# class OAuth2Validator(OrigOAuth2Validator):
#     def rotate_refresh_token(self, request):
#         '''IFTTT Requires our refresh_tokens to be reusable, thus we don't
#         rotate them'''
#         return False


def customer_get_shops(request):
    shops = ShopSerializer(
        Shop.objects.all().order_by("-id"),
        many = True,
        context = {"request":request}
    ).data

    return JsonResponse({"shops": shops})


def customer_get_shop_items(request, shop_id):
    items = ItemSerializer(
        Item.objects.filter(shop_id = shop_id).order_by("-id"),
        many = True,
        context = {"request":request}
    ).data
    return JsonResponse({"items": items})


@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token:test123
            shop_id:1
            address:test123
            order_details: [{"item_id":1, "quantity":2},{"item_id":2, "quantity":1}]
    """

    if request.method == "POST":
        #Get Token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

        #Get Customer
        customer = access_token.user.customer

        #Check whether if customer had any other order not delivered
        #-- Alpha , Beta only should be able to add in more orders
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({
                "status" : "failed",
                "error" : "Your last order must be completed"
            })

        #Check the address
        if not request.POST["address"]:
            return JsonResponse({
                "status" : "failed",
                "error" : "Address is required"
            })  

        #Get Order details
        order_details  = json.loads(request.POST["order_details"])

        order_total = 0
        for item in order_details:
            order_total += Item.objects.get(id = item["item_id"]).price * item["quantity"]

        if len(order_details) > 0:
            #Step 1 -  Create an order
            order = Order.objects.create(
                customer = customer,
                shop_id = request.POST["shop_id"],
                total = order_total,
                status = Order.ORDERED,
                address = request.POST["address"]
            )

            #Step2 - Create an order_details
            for item in order_details:
                OrderDetail.objects.create(
                    order = order,
                    item_id = item["item_id"],
                    qty = item["quantity"],
                    sub_total = Item.objects.get(id = item["item_id"]).price * item["quantity"]
                )

            return JsonResponse({"status": "success"})    



def customer_latest_order(request):

    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    #Get Customer
    customer = access_token.user.customer

    order = OrderSerializer(Order.objects.filter(customer=customer).last()).data

    return JsonResponse({"order":order})



def shop_order_notification(request, last_request_time):
    notification = Order.objects.filter(
        shop = request.user.shop,
        created_at__gt = last_request_time
    ).count()
    return JsonResponse({"notification" : notification})