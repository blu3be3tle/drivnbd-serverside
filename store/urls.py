from .views import ProductViewSet, ReviewViewSet, OrderViewSet, WishlistAPIView, AdminStatsAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')

products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('wishlist/', WishlistAPIView.as_view(),
         name='wishlist'),
    path('admin/stats/', AdminStatsAPIView.as_view(),
         name='admin-stats'),
]
