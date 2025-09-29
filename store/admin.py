from django.contrib import admin
from .models import Product, Color, Size, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'average_rating')
    search_fields = ('name',)


admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Review)
