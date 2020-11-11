from django.contrib.auth import get_user_model
from recipes.models import Favorite, Product, Purchase, Subscription
from rest_framework import serializers

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']


class SubscriptionsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Subscription
        fields = ['user', 'author']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'dimension']


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Purchase
        fields = ['user', 'recipe']
