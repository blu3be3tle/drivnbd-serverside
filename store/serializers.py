# store/serializers.py
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from .models import Product, Review, Color, Size, Order, OrderItem, Wishlist


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "name", "price", "image", "average_rating"]
        read_only_fields = ["id", "average_rating", "image"]


class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    image = serializers.ImageField(read_only=True)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "colors",
            "sizes",
            "stock",
            "average_rating",
            "reviews",
        ]
        read_only_fields = ["id", "image", "average_rating", "reviews"]


# Orders
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]
        read_only_fields = ["price"]

    def validate_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError(
                "Quantity must be a positive integer.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "items", "total_price", "status", "created_at"]
        read_only_fields = ["id", "user",
                            "total_price", "status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        if not items_data:
            raise serializers.ValidationError(
                {"items": "At least one item is required."})

        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Authenticated user required.")

        with transaction.atomic():
            order = Order.objects.create(user=user, status="PENDING")

            total_price = Decimal("0.00")

            for item in items_data:
                product = item["product"]
                quantity = int(item["quantity"])

                locked_product = (
                    Product.objects.select_for_update()
                    .only("id", "price", "stock")
                    .get(pk=product.pk)
                )

                if locked_product.stock < quantity:
                    raise serializers.ValidationError(
                        {
                            "items": [
                                {
                                    "product": locked_product.pk,
                                    "detail": "Insufficient stock.",
                                    "available": locked_product.stock,
                                }
                            ]
                        }
                    )

                unit_price = locked_product.price
                line_total = unit_price * quantity
                total_price += line_total

                OrderItem.objects.create(
                    order=order,
                    product=locked_product,
                    quantity=quantity,
                    price=unit_price,
                )

                locked_product.stock = F("stock") - quantity
                locked_product.save(update_fields=["stock"])

            order.total_price = total_price.quantize(Decimal("0.01"))
            order.save(update_fields=["total_price"])

        return order


# Wishlist
# store/serializers.py
class WishlistSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']
