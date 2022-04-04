from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag, Recipe, Ingredient, Favorite, RecipeIngredient
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, CreateRecipeSerializer, \
    FavoriteSerializer, ShoppingCartSerializer


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


class FavoriteApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, favorite_recipe_id):
        user = request.user
        data = {
            'recipe': favorite_recipe_id,
            'user': user.id
        }
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, favorite_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=favorite_id)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, shc_recipe_id):
        user = request.user
        data = {
            'recipe': shc_recipe_id,
            'user': user.id
        }
        serializer = ShoppingCartSerializer(
            data=data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, shc_recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=favorite_id)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    def get(self, request):
        final_list = {}
        ingredients = RecipeIngredient.objects.filter(recipe__shoping_cart__user=request.user)
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
