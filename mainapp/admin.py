from django.contrib import admin

from .models import Fridge_model, Generate_Recepts, Ingridients, Product, Products, Recepts,Favourites


@admin.register(Fridge_model)
class Fridge_admin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']
    


@admin.register(Product)
class Product_admin(admin.ModelAdmin):

    list_filter = ['name_product']
    
admin.site.register(Products)
admin.site.register(Recepts)
admin.site.register(Ingridients)
admin.site.register(Generate_Recepts)
admin.site.register(Favourites)