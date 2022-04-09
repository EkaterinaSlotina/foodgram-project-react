from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet, RecipeViewSet, IngredientViewSet,
    FavoriteApiView, ShoppingCartApiView, DownloadShoppingCart
)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='reciepes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(), name='download'
    ),
    path('', include(router.urls)),
    path(
        'recipes/<int:pk>/favorite/',
        FavoriteApiView.as_view(), name='favorite'
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        ShoppingCartApiView.as_view(), name='shopping'
    ),
]
