from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='имя')
    color = models.CharField(
        max_length=7, default="#ffffff", verbose_name='цвет'
    )
    slug = models.SlugField(max_length=200, verbose_name='слаг')

    class Meta:
        verbose_name = 'тег'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='имя')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='единица измерения'
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    name = models.CharField(max_length=200, verbose_name='имя')
    image = models.ImageField(
        upload_to='photos/', blank=True, null=True,
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipe_to_ingredient',
        verbose_name='ингредиент')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='тэг')
    cooking_time = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='время приготовления')

    class Meta:
        verbose_name = 'рецепт'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_to_recipe',
        verbose_name='ингредиент')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_to_recipe',
        verbose_name='рецепт')
    amount = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='ingredient_to_recipe'
            )
        ]
        verbose_name = 'ингредиент в рецепте'

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='favorite_unique'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_cart',
        verbose_name='покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='shopping_cart_unique'
            )
        ]
