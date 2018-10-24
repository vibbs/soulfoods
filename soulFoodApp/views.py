from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from soulFoodApp.forms import UserForm, ShopForm
# Create your views here.


def home(request):
    return redirect(shop_home)

@login_required(login_url='/shop/sign-in/')
def shop_home(request):
    return render(request, 'shop/home.html', {})    


def shop_sign_up(request):
    user_form = UserForm()
    shop_form = ShopForm()
    return render(request, 'shop/sign-up.html', {
        'user_form' : user_form,
        'shop_form' : shop_form
    })    
