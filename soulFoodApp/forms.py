from django import forms
from django.contrib.auth.models import User
from soulFoodApp.models import Shop, Item


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = {"username", "password", "first_name", "last_name", "email"}


class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = {"first_name", "last_name", "email"}

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = {"shop_name", "address", "phone", "logo"}

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ("shop",)