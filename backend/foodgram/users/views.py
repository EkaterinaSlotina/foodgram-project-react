from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Subscription
from .serializers import SubscriptionSerializer, SubscriptionListSerializer


class SubscribeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, following_id):
        user = request.user
        data = {
            'following': following_id,
            'user': user.id
        }
        serializer = SubscriptionSerializer(data=data,
                                          context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, following_id):
        user = request.user
        following = get_object_or_404(User, id=following_id)
        Subscription.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsApiView(APIView):
    serializer_class = SubscriptionListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
