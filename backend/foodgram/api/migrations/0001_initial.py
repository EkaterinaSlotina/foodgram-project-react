# Generated by Django 3.0.5 on 2022-03-14 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')
                 ),
                ('name', models.CharField(max_length=200)),
                ('measurement_unit', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')
                 ),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(
                    blank=True, null=True, upload_to='photos/',
                    verbose_name='Картинка')
                 ),
                ('text', models.TextField(
                    help_text='Введите текст', verbose_name='Текст')
                 ),
                ('cooking_time', models.PositiveIntegerField(
                    blank=True, null=True)
                 ),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')
                 ),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(
                    default='#ffffff', max_length=7)
                 ),
                ('slug', models.SlugField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')
                 ),
                ('amount', models.PositiveIntegerField(
                    blank=True, null=True)
                 ),
                ('ingredient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='api.Ingredient')
                 ),
                ('recipe', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='api.Recipe')
                 ),
            ],
        ),
    ]
