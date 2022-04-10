from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.models import Recipe


class GetMixin:
    def get(self, request, pk):
        user = request.user
        data = {
            'recipe': pk,
            'user': user.id
        }
        serializer = self.serializer_class(
            data=data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteMixin:
    def delete(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        self.model.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
