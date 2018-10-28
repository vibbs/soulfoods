from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from soulFoodApp import views, apis


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),


    #SHOP based endpoints
    url(r'^shop/sign-in/$', auth_views.login, 
        {'template_name': 'shop/sign-in.html'},
        name = 'shop-sign-in'),
    url(r'^shop/sign-out/$', auth_views.logout,
        {'next_page': '/'},
        name = 'shop-sign-out'),
    url(r'^shop/$', views.shop_home, name = 'shop-home'),
    url(r'^shop/sign-up/$', views.shop_sign_up,
        name = 'shop-sign-up'),

    url(r'^shop/account/$', views.shop_account, name = 'shop-account'),
    url(r'^shop/item/$', views.shop_item, name = 'shop-item'),
     url(r'^shop/item/add/$', views.shop_add_item, name = 'shop-add-item'),
     url(r'^shop/item/edit/(?P<item_id>\d+)/$', views.shop_edit_item, name = 'shop-edit-item'),
    url(r'^shop/order/$', views.shop_order, name = 'shop-order'),
    url(r'^shop/report/$', views.shop_report, name = 'shop-report'),

    #APIS for CUSTOMERS
    url(r'api/customer/shops/$', apis.customer_get_shops),
    url(r'api/customer/shops/items/(?P<shop_id>\d+)/$', apis.customer_get_shop_items),
    url(r'api/customer/order/add/$', apis.customer_add_order),
    url(r'api/customer/order/latest/$', apis.customer_latest_order),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
