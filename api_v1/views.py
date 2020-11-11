from django.contrib.auth import get_user_model
from recipes.models import Favorite, Product, Purchase, Subscription
from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (FavoriteSerializer, ProductSerializer,
                          PurchaseSerializer, SubscriptionsSerializer)

User = get_user_model()


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favorite, recipe=kwargs.get('pk'), user=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Subscription, author=kwargs.get('pk'), user=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            instance = serializer.data.get('recipe')
            self.request.session.setdefault('purchases', [])
            self.request.session['purchases'].append(instance)
            self.request.session.save()

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            instance = get_object_or_404(
                Purchase, recipe=kwargs.get('pk'), user=request.user)
            self.perform_destroy(instance)
        else:
            instance = int(kwargs.get('pk'))
            request.session['purchases'].remove(instance)
            request.session.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$title']
