from django.contrib import admin
from .models import Product, Order, OrderItem, Color, Size, Review, Wishlist


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('user__email', 'id')
    inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'average_rating')
    search_fields = ('name',)


admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Review)
admin.site.register(Wishlist)
