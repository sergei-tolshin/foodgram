from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, ProductViewSet, PurchaseViewSet,
                    SubscriptionsViewSet)

router = DefaultRouter()
router.register('ingredients', ProductViewSet, basename='ingredients')
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('purchases', PurchaseViewSet, basename='purchases')
router.register('subscriptions', SubscriptionsViewSet,
                basename='subscriptions')


urlpatterns = [
    path('', include(router.urls)),
]
