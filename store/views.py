from .serializers import WishlistSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Review, Order, Wishlist
from .serializers import ProductListSerializer, ProductDetailSerializer, ReviewSerializer, OrderSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sizes__name', 'colors__name']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['product_pk'])
        serializer.save(user=self.request.user, product=product)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}




class WishlistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
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

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
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

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.remove(product)
        return Response({'status': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)
