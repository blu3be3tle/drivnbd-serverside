# store/views.py

from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Review, Order, Wishlist
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    ReviewSerializer, OrderSerializer, WishlistSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sizes__name', 'colors__name']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        return ProductListSerializer if self.action == 'list' else ProductDetailSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        product_pk = self.kwargs.get('product_pk')
        if product_pk:
            return Review.objects.filter(product_id=product_pk)
        return Review.objects.none()

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['product_pk'])
        serializer.save(user=self.request.user, product=product)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user).order_by('-created_at')
        return Order.objects.none()

    def get_serializer_context(self):
        return {'request': self.request}


class WishlistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        return Response({'status': 'Product added to wishlist.'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.remove(product)
        return Response({'status': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)


class AdminStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        one_week_ago = today - timedelta(days=7)
        one_month_ago = today - timedelta(days=30)

        # Purchases
        purchases_last_week = Order.objects.filter(
            created_at__gte=one_week_ago).count()
        purchases_last_month = Order.objects.filter(
            created_at__gte=one_month_ago).count()

        # Sales totals
        total_sell_current_month = Order.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month
        ).aggregate(total=Sum('total_price'))['total'] or 0

        prev_month = today.month - 1 if today.month > 1 else 12
        prev_month_year = today.year if today.month > 1 else today.year - 1

        total_sell_previous_month = Order.objects.filter(
            created_at__year=prev_month_year,
            created_at__month=prev_month
        ).aggregate(total=Sum('total_price'))['total'] or 0

        # Products
        most_liked_products = Product.objects.annotate(
            wishlist_count=Count('wishlist__id', distinct=True)
        ).order_by('-wishlist_count')[:5]

        # Users with most orders
        top_buying_users = get_user_model().objects.annotate(
            orders_count=Count('orders', distinct=True)
        ).filter(orders_count__gt=0).order_by('-orders_count')[:5]

        data = {
            'purchases': {
                'last_week': purchases_last_week,
                'last_month': purchases_last_month,
            },
            'sales': {
                'current_month_total': total_sell_current_month,
                'previous_month_total': total_sell_previous_month,
            },
            'top_products': ProductListSerializer(most_liked_products, many=True).data,
            'top_users': [
                {'email': user.email, 'orders': getattr(
                    user, 'orders_count', 0)}
                for user in top_buying_users
            ]
        }
        return Response(data)
