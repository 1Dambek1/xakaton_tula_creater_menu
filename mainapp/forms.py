from typing import Any

from django import forms

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User

from .models import Fridge_model, Product, Products,Recepts


from django.core.exceptions import ValidationError




class Login_Form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"input",'type':"text" }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'required':'','class':"input",'type':"password",'data-hide-password-input':''}))
    class Meta:
        model = User
        fields = ['username','password']
        
class Register_Form(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"input",'type':"text" }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'required':'','class':"input",'type':"password",'data-hide-password-input':''}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'required':'','class':"input",'type':"password",'data-hide-password-input':''}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        



class CreateProductForm(forms.ModelForm):
    name_product =forms.CharField(widget=forms.TextInput(attrs={"name":"product_name","type":"text","class":"form-module__input input"}))
    img = forms.ImageField(widget=forms.FileInput(attrs={"type":"file" ,"class":"file"}),required=False)
    weight = forms.ChoiceField(choices=[('л', 'литр'),('Kg', 'kg'),('шт', 'штук')], widget = forms.Select(attrs={"class":"form-module__item select"}))
    expiration_date_days =forms.IntegerField(widget=forms.NumberInput(attrs={"name":"expiration_date_days","type":"number","class":"form-module__input input"}))
    class Meta:
        model = Product
        fields = ['name_product', 'img','weight','expiration_date_days','creater']

class UpdateProductsForm(forms.ModelForm):
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'name':"product_name",'type':"text",'class':"form-module__input input product-name ", "label":'Какое колличество продукта(кг,л,шт)'}))
    
    class Meta:
        model = Products
        fields = ['fridge','product','weight']

class MinMaxTimeForm(forms.Form):

    names = forms.CharField(required=False,widget=forms.TextInput(attrs={}))
    
    min_cal= forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class':"form-filter__input input"}))
    max_cal = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class':"form-filter__input input"}))
    
    
    
    

