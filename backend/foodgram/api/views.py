from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import (
    Tag, Recipe, Ingredient, Favorite,
    RecipeIngredient, ShoppingCart
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    TagSerializer, RecipeSerializer, IngredientSerializer,
    CreateRecipeSerializer, FavoriteSerializer, ShoppingCartSerializer
)
from .utils import GetMixin, DeleteMixin


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return CreateRecipeSerializer
        return RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get']
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]


class FavoriteApiView(GetMixin, DeleteMixin, APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FavoriteSerializer
    model = Favorite

    def get_favorite(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete_favorite(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ShoppingCartApiView(GetMixin, DeleteMixin, APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShoppingCartSerializer
    model = ShoppingCart

    def get_shopping_cart(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete_shopping_cart(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class DownloadShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        final_list = 'Список покупок:\n\n'
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
        ).annotate(total_amount=Sum('amount'))
        for position, ingredient in enumerate(ingredients, start=1):
            final_list.append(
                f'{ingredient["ingredient__name"]}:'
                f'{ingredient["total_amount"]}'
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )
        response = HttpResponse(final_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response
