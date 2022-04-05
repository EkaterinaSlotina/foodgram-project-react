from django.http import HttpResponse
from rest_framework import viewsets, filters, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Tag, Recipe, Ingredient, Favorite, RecipeIngredient, ShoppingCart
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    TagSerializer, RecipeSerializer, IngredientSerializer, CreateRecipeSerializer,
    FavoriteSerializer, ShoppingCartSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return CreateRecipeSerializer
        return RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get']


class FavoriteApiView(mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView
                      ):
    permission_classes = [IsAuthenticated, ]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ShoppingCartApiView(mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          generics.GenericAPIView
                          ):
    permission_classes = [IsAuthenticated, ]
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DownloadShoppingCart(APIView):
    def get(self, request):
        final_list = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoping_cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount')
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
            }
            else:
                final_list[name]['amount'] += item[2]
        response = HttpResponse(final_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response
