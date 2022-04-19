from rest_framework import serializers

from .models import User, Subscription
from api.serializers import RecipeShortSerializer


class SubscriptionListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        ]

    def get_is_subscribed(self, user):
        current_user = self.context.get('request').user
        other_user = user.following.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        return Subscription.objects.filter(
            user=user, following=current_user
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:3]
        request = self.context.get('request')
        return RecipeShortSerializer(
            recipes, many=True,
            context={'request': request}
        ).data


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'following')

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscriptionListSerializer(
            instance.following,
            context={'request': request}
        ).data
