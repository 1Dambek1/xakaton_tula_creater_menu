from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.contrib.postgres.fields import ArrayField


class Fridge_model(models.Model):

    
    user = models.OneToOneField(to = User, on_delete=models.CASCADE)



    
    def __str__(self) -> str:
        return f"{self.user} - Пользователь холодильника"

    class Meta:
        verbose_name = 'Холодильник'
        verbose_name_plural = 'Холодильники'
        
        
class Product(models.Model):
    
    WEIGHT = [('л', 'литр'),('Kg', 'kg'),('шт', 'штук')]

    
    name_product = models.CharField(max_length=255)
    
    img = models.ImageField(upload_to='proudct_img', blank=True)
    
    weight = models.CharField(choices=WEIGHT, max_length=3)
    
    expiration_date_days = models.IntegerField(blank=True, null = True)    
    
    creater = models.ForeignKey(to = User,on_delete=models.CASCADE, blank=True, default=None, null=True)
    
    def __str__(self) -> str:
        return f"{self.name_product} "

    class Meta:
        verbose_name = 'Список продуктов'
        verbose_name_plural = 'Продукты'
    
class Products(models.Model):
    fridge = models.ForeignKey(to =Fridge_model, on_delete=models.CASCADE)
    
    product = models.OneToOneField(to = Product, on_delete=models.CASCADE)
    
    weight = models.FloatField()
    def __str__(self) -> str:
        return f"{self.product.name_product} | {self.fridge.user} "

    class Meta:
        verbose_name = 'Продукт в Холодильнику'
        verbose_name_plural = 'Продукты в Холодильнике'

    
class Ingridients(models.Model):
    
    product = models.ForeignKey(to = Product, on_delete=models.CASCADE)
    how_many = models.FloatField()
    
    def __str__(self) -> str:
        return f"{self.product.name_product}"

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
    
class Recepts(models.Model):
    TIME = [('h', 'hours'), ('m', 'minutes'), ('d', 'days')]
    
    products = models.ManyToManyField(to = Ingridients)
    img = models.ImageField(upload_to='recepts', null=True)
    
    name = models.CharField(max_length=255)
    
    calories  = models.IntegerField()
    
    which_time = models.CharField(choices=TIME, max_length=1)
    
    Time_to_create = models.IntegerField()
    
    script = models.TextField()
    
    creater = models.ForeignKey(to = User, on_delete=models.CASCADE, blank=True, default=None,null=True)
    
    portion = models.SmallIntegerField()
    time = models.CharField(max_length=255, choices=[('breakfast','breakfast'),('lunch','lunch'), ('dinner','dinner')], null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    
    def clean(self) -> None:
        valid =  super().clean()
        
        if self.calories >0 :
            return valid
        return ValidationError({'calories':'must be more than 0 '})


class Favourites(models.Model):
    user = models.ForeignKey(to = User, on_delete=models.CASCADE)
    recept = models.ForeignKey(to=Recepts, on_delete=models.CASCADE)   

    def __str__(self) -> str:
        return f"{self.user} | {self.recept}"

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные' 


class Generate_Recepts(models.Model):
    user = models.ForeignKey(to = User, on_delete=models.CASCADE)
    

    script = models.TextField()
    ingridents =ArrayField( ArrayField(models.CharField(max_length=255)), null=True)
    calories = models.IntegerField()
    time = models.TextField(choices=[('breakfast','breakfast'),('lunch','lunch'),('dinner','dinner')])

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = 'Рецепт от ai' 
        verbose_name_plural = 'Рецепты от ai'
