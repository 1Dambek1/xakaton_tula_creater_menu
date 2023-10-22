
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from .views import  AddProductView, create_menu_with_ai,FridgeView, ReceptsFilterView, delete_product,UpdateProductsView,CreateProductView,TrainView,cooked,delete_ai,make_favourite,delete_favourite,FavouriteView,logouts
app_name = 'main'
urlpatterns = [

    path('fridge',FridgeView.as_view(), name = 'fridge'),
    path('update_quantity/<int:pk_product>', UpdateProductsView.as_view(), name = 'update'),
    path('add_product', AddProductView.as_view(), name='add_product'),
    path('create_product', CreateProductView.as_view(), name='create_product'),
    path('delete_product/<int:id_product>', delete_product, name = 'delete'),
    path('add_product/<int:id_product>',AddProductView.as_view(), name='add_product_main'),

    
    path('filter/<str:which_time>', ReceptsFilterView.as_view(), name = 'filter'),
    path('train/<int:calories>', TrainView.as_view(), name = 'train'),
    path('generic_ai/<str:true>/<int:cal>/<str:which_time>',create_menu_with_ai, name='generic_recept'),
    path('cook/<int:id_recept>', cooked, name = 'cook'),
    path('delete_ai/<int:id_ai>', delete_ai, name = 'delete_ai'),
    
    path('make_fovurite/<int:recept_id>',make_favourite, name = 'make_f'),
    path('delete_fovurite/<int:recept_id>',delete_favourite, name = 'delete_f'),
    path('favourites', FavouriteView.as_view(), name = 'favourite'),
    
    
    path('<str:ingridients>/<int:cal>/<str:which_time>', create_menu_with_ai),
    path('delete_product/<int:id_product>', delete_product, name= 'deleteproduct'),
    

]