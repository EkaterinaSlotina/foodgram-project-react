# Generated by Django 3.2.9 on 2022-04-04 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_recipeingredient_ingredient_to_recipe'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscribe',
        ),
    ]
