from rest_framework import viewsets, serializers
from inventory.models import product
from inventory.models import Transaction

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'