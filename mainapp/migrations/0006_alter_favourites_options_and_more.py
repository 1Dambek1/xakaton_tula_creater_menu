# Generated by Django 4.2.5 on 2023-10-22 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_remove_generate_recepts_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourites',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранные'},
        ),
        migrations.AlterModelOptions(
            name='generate_recepts',
            options={'verbose_name': 'Рецепт от ai', 'verbose_name_plural': 'Рецепты от ai'},
        ),
        migrations.AlterModelOptions(
            name='ingridients',
            options={'verbose_name': 'Ингридиент', 'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Список продуктов', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'Продукт в Холодильнику', 'verbose_name_plural': 'Продукты в Холодильнике'},
        ),
        migrations.AlterModelOptions(
            name='recepts',
            options={'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
    ]
