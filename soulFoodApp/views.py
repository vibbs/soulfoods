from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from soulFoodApp.forms import UserForm, ShopForm, UserFormForEdit, ItemForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from soulFoodApp.models import Item


# Create your views here.

def home(request):
    return redirect(shop_home)

@login_required(login_url='/shop/sign-in/')
def shop_home(request):
    return redirect(shop_order)

@login_required(login_url='/shop/sign-in/')
def shop_account(request):
    user_form = UserFormForEdit(instance = request.user)
    shop_form = ShopForm(instance = request.user.shop)

    if request.method == "POST" :
        user_form = UserFormForEdit(request.POST, instance = request.user)
        shop_form = ShopForm(request.POST, request.FILES, instance = request.user.shop)

        if user_form.is_valid() and shop_form.is_valid():
            user_form.save()
            shop_form.save()

    return render(request, 'shop/account.html', {
        "user_form" :user_form,
        "shop_form" :shop_form
    })  

@login_required(login_url='/shop/sign-in/')
def shop_item(request):
    items = Item.objects.filter(shop = request.user.shop).order_by("-id")
    return render(request, 'shop/item.html', {"items" : items})  

@login_required(login_url='/shop/sign-in/')
def shop_add_item(request):
    item_form = ItemForm()

    if request.method == "POST" :
        item_form = ItemForm(request.POST, request.FILES)

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.shop = request.user.shop
            item.save()

            return redirect(shop_item)

    return render(request, 'shop/add-item.html', {
        "item_form" :item_form
    })     

@login_required(login_url='/shop/sign-in/')
def shop_edit_item(request, item_id):
    item_form = ItemForm(instance = Item.objects.get(id = item_id))

    if request.method == "POST" :
        item_form = ItemForm(request.POST, request.FILES, instance = Item.objects.get(id = item_id))

        if item_form.is_valid():
            item_form.save()
            return redirect(shop_item)

    return render(request, 'shop/edit-item.html', {
        "item_form" :item_form
    })          

@login_required(login_url='/shop/sign-in/')
def shop_order(request):
    return render(request, 'shop/order.html', {})  

@login_required(login_url='/shop/sign-in/')
def shop_report(request):
    return render(request, 'shop/report.html', {})  
    

def shop_sign_up(request):
    user_form = UserForm()
    shop_form = ShopForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        shop_form = ShopForm(request.POST, request.FILES)

        if user_form.is_valid() and shop_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data) #** is to make sure we get clean data
            new_shop = shop_form.save(commit=False)
            new_shop.user = new_user
            new_shop.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(shop_home)

    return render(request, 'shop/sign-up.html', {
        'user_form' : user_form,
        'shop_form' : shop_form
    })    


    