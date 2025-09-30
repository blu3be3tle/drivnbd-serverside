from django.urls import path, include

urlpatterns = [
    path('products/', include('store.product_urls')),
    path('categories/', include('store.category_urls'))
]
