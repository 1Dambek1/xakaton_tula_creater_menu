from django.contrib.auth.decorators import login_required
from typing import Any
from django import http
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms import formset_factory
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.db.models import Q
from .models import Favourites, Fridge_model, Generate_Recepts, Ingridients, Product, Products,Recepts
from .forms import *
import numba
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginsView(LoginView):
    form_class = Login_Form
    template_name = 'mainapp/login.html'
    success_url = reverse_lazy('main:fridge')
    def get_success_url(self) -> str:
        return reverse_lazy('main:fridge')
    
class RegisterView(CreateView):
    model = User
    form_class = Register_Form
    template_name = 'mainapp/registry.html'
    # success_url = reverse_lazy('login')
    def get_success_url(self) -> str:
        return reverse_lazy('main:fridge')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:

        a = form.save()
        login(self.request, a)
        if not Fridge_model.objects.filter(user = a).exists():
            Fridge_model.objects.create(user = a)
        return redirect('main:fridge')
    

class FridgeView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/ingredients.html'

    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        gets = super().get(request, *args, **kwargs)
        
        fridge = get_object_or_404(Fridge_model, user = request.user)
        
        products = Products.objects.filter(fridge = fridge)
        
        

        return self.render_to_response({'fridge':fridge, 'products':products})
    


class CreateProductView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/createProduct.html'
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        a =  super().get(request, *args, **kwargs)
        form = CreateProductForm()
        return self.render_to_response({'form':form})
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        datas = request.POST
        form  = CreateProductForm(data={'creater':request.user,'expiration_date_days':datas.get('expiration_date_days'),'weight':datas.get('weight'),'name_product':datas.get('name_product'),'img':datas.get('img')}, files=request.FILES)
        
        if form.is_valid():
            form.save()
        return redirect(reverse('main:create_product'))

class UpdateProductsView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp\changeProductQuantity.html'
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        products = get_object_or_404(Products,pk = self.kwargs.get('pk_product') , fridge =Fridge_model.objects.get(user = request.user) )
        form = UpdateProductsForm(initial = {'weight':products.weight, 'product':products.product, 'fridge':products.fridge})
        return self.render_to_response({'form':form, 'product':products})
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        products = get_object_or_404(Products,pk = self.kwargs.get('pk_product') , fridge =Fridge_model.objects.get(user = request.user) )
        form = UpdateProductsForm( data = {'fridge':products.fridge, 'product':products.product,'weight':request.POST.get('weight')})
        if float(request.POST.get('weight')) <=0:
            products.delete()
        else:
            products.weight =request.POST.get('weight')
            products.save()
        return redirect(reverse('main:fridge'))
 
class AddProductView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/addProduct.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        all_products = []
        all_products1 = Product.objects.filter(creater = None)
        all_products2 = Product.objects.filter(creater = request.user)
        try:
            id_product = Product.objects.get(pk=self.kwargs.get('id_product'))
            print('yes')
            if id_product:
                print('yes')
                form = UpdateProductsForm()
                return self.render_to_response({'all_prod':all_products, 'form':form, 'product':id_product})
        except:pass
        for i in all_products1:
            all_products.append(i)
        for i in all_products2:
            all_products.append(i)

        
        return self.render_to_response({'all_prod':all_products})
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        product = get_object_or_404(Product, pk = self.kwargs.get('id_product'))
        products = Products.objects.filter(product = product)
        if products.exists():
            products = products.first()
            products.weight += int(request.POST.get('weight'))
            products.save()
        else:
            Products.objects.create(weight = request.POST.get('weight'), fridge = Fridge_model.objects.get(user = request.user), product = product)
        return redirect(reverse('main:add_product'))
            
 
 
             
class ReceptsFilterView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/breakfast.html'
    
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        gets =  super().get(request, *args, **kwargs)
        
        which_time = self.kwargs.get('which_time')
        
        times = {'breakfast':'завтрак','lunch':'обед', 'dinner':'ужин'}
        

        if which_time in ('breakfast', 'lunch', 'dinner'):
            ai_recepts = Generate_Recepts.objects.filter(user = request.user, time = which_time)
            
            search = self.request.GET.get('search')
            
            min_col = int(self.request.GET.get('min_col')) if self.request.GET.get('min_col') else None
            max_col = int(self.request.GET.get('max_col')) if self.request.GET.get('max_col') else None
            
            true = request.GET.get('true').replace('+', ' ').split('-') if  request.GET.get('true') else None
            
            recepts = []
            products_in_fridge = Products.objects.filter(fridge = Fridge_model.objects.get(user = request.user))
            
            
            if min_col!=None and max_col!=None:
                recepts2  = Recepts.objects.filter(calories__gte = min_col , calories__lte =max_col, time = which_time )
                for i in recepts2:
                            recepts.append(i)
            if true:
                recept_search =  recepts2.filter(time = which_time)
                for i in recept_search:
                        mass = [i2.product.name_product for i2 in i.products.all()]
                        for i3 in true:
                            if i3 in mass:
                                recepts.append(i)
                                break        
                                    
            if search:
                recept_search =  Recepts.objects.filter(name__icontains = search, time =which_time)
                for i in recept_search:
                    recepts.append(i)
            if not search and not true and  min_col==None and max_col==None:
                recepts = Recepts.objects.filter(time =which_time)
            
            else:
                recepts = list(set(recepts))
                
                
                    
            

                
            

            return self.render_to_response({'products':products_in_fridge,'recepts':recepts,'true':str(true) if true else str(['яйца']), 'cal':round((min_col+max_col)/2) if min_col and max_col else 200, 'ai':ai_recepts,'time':times.get(which_time), 'izbran':[i.recept for i in (Favourites.objects.filter(user = request.user))]})
        else:
            raise 404
        
      
        
        
class FavouriteView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/favorite.html'
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        favour= Favourites.objects.filter(user = request.user)
        
        return self.render_to_response({'favour':favour})


class TrainView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/trainee.html'
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        import g4f
        def ai_answer(comment: str):

            response=  g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages =[{'role':"user", "content":comment}],

                
                
            )
            return response
        col = self.kwargs.get('calories')
        script = ai_answer(f'Сделай мне тренировку для сжигания минимум {col} калорий ')
        while script == '当前地区当日额度已消耗完':
            script = ai_answer(f'Сделай мне тренировку для сжигания минимум {col} калорий ')
        return self.render_to_response({'ai':script, 'col':col})
@login_required
def delete_product(request, id_product):
    product = get_object_or_404(Products, pk = id_product)
    
    if product.fridge.user == request.user:
        product.delete()
    return redirect(reverse('main:fridge'))
@login_required
def make_favourite(request, recept_id):
    recept = get_object_or_404(Recepts, pk = recept_id)
    if not Favourites.objects.filter(recept = recept, user = request.user).exists():
        
        Favourites.objects.create(user = request.user, recept = recept)
    return redirect(reverse('main:filter',kwargs={'which_time':recept.time}))
@login_required
def delete_favourite(request, recept_id):
    recept = get_object_or_404(Recepts, pk = recept_id)
    favor = get_object_or_404(Favourites,recept = recept, user = request.user)
    favor.delete()
    return redirect(reverse('main:filter',kwargs={'which_time':recept.time}))
@login_required
def delete_ai(request, id_ai):
    ai =get_object_or_404(Generate_Recepts, pk = id_ai, user = request.user)
    ai.delete()
    return redirect(reverse('main:filter' , kwargs={"which_time" : ai.time}))
@login_required
def create_menu_with_ai(request, true, cal, which_time):
    import g4f
    def ai_answer(comment: str):

        response=  g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages =[{'role':"user", "content":comment}],

            
            
        )
        return response

    if which_time in ('завтрак', 'обед', 'ужин'):
        time = {'завтрак':'breakfast', 'обед':'lunch', 'ужин':'dinner'}


        true= true[1:-1]
        true=  true.replace("'", '')
        true = true.replace('"', '')
        true = true.replace(' ', '')
        true = true.split(',')
        
        script = ai_answer(f'Сделай мне быстро рецепт создания блюда на {which_time} используя ингридиенты  {true} калорийностью {int(cal)}')
        while script == '当前地区当日额度已消耗完':
            script = ai_answer(f'Сделай мне быстро рецепт создания блюда на {which_time} используя ингридиенты  {true} калорийностью {int(cal)}')
        Generate_Recepts.objects.create(user = request.user,script = script, ingridents = true, calories = round(int(cal)), time = time.get(which_time))
    return redirect(reverse('main:filter',kwargs={'which_time':time.get(which_time)}))



@login_required
def cooked(request, id_recept):
    recept = get_object_or_404(Recepts, pk = id_recept)
    
    fridge = get_object_or_404(Fridge_model, user = request.user)
    products = Products.objects.filter(fridge = fridge)
    
    for i in recept.products.all():
        product_fridge = Products.objects.filter(product = i.product,fridge = fridge)
        if product_fridge.exists():
            product_fridge = product_fridge.first()
            
            product_fridge.weight -= i.how_many
            if product_fridge.weight <=0:
                product_fridge.delete()
            else:
                product_fridge.save()
    
    return redirect(reverse('main:filter',kwargs={'which_time':recept.time}))


def logouts(request):
    logout(request)
    return redirect('login')


class CreateReceptView(LoginRequiredMixin,TemplateView):
    template_name = 'mainapp/create-recept.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        gets =  super().get(request, *args, **kwargs)
        