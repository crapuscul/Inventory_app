from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from inventory.models import product
from inventory.models import Transaction
from .serializers import ProductSerializer, TransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

class InventoryUpdateView(APIView):
    def patch(self, request, pk):
        product_instance = get_object_or_404(product, product_id=pk)
        if product_instance:
            product_instance.product_quantity -= 1  # Adjust as needed
            product_instance.save()
            serializer = ProductSerializer(product_instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Product not found'}, status=404)

class ProductList(generics.ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        # Custom logic to update inventory based on the products in the transaction
        product_instances = serializer.validated_data.get('products',[])

        for product_instance in product_instances:
            product_instance .product_quantity -= 1
            product_instance.save()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



