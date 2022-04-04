from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet, IngredientViewSet, FavoriteApiView, ShoppingCartApiView, \
    DownloadShoppingCart

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='reciepes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:favorite_recipe_id>/favorite/', FavoriteApiView.as_view()),
    path('recipes/<int:shc_recipe_id>/shopping_cart/', ShoppingCartApiView.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view() )
]
