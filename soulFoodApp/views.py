from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from soulFoodApp.forms import UserForm, ShopForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return redirect(shop_home)

@login_required(login_url='/shop/sign-in/')
def shop_home(request):
    return render(request, 'shop/home.html', {})    

@login_required(login_url='/shop/sign-in/')
def shop_account(request):
    return render(request, 'shop/account.html', {})  

@login_required(login_url='/shop/sign-in/')
def shop_item(request):
    return render(request, 'shop/item.html', {})  

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


    