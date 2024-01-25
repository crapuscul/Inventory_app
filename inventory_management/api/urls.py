# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, InventoryUpdateView, TransactionViewSet, ProductList, ProductDetail

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'transactions', TransactionViewSet, basename='transaction')  # New endpoint for transactions

urlpatterns = [
    path('inventory/update/<int:pk>/', InventoryUpdateView.as_view(), name='inventory-update'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('', include(router.urls)),
]
