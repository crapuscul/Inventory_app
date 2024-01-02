# inventory/forms.py
from django import forms
from .models import product, family, subfamily


class FamilyForm(forms.ModelForm):
    class Meta:
        model = family
        fields = ['family_name']

class SubFamilyForm(forms.ModelForm):
    class Meta:
        model = subfamily
        fields = ['subfamily_name']

    family = forms.ModelChoiceField(
        queryset=family.objects.all(),
        empty_label='Select a Family',
        label='Family',
    )

class SubFamilyEditForm(forms.ModelForm):
    class Meta:
        model= subfamily
        fields = ['subfamily_name','family']

    family = forms.ModelChoiceField(
            queryset=family.objects.all(),
            empty_label='Select a Family',
            label='Family',
    )

class ProductForm(forms.ModelForm):


    family = forms.ModelChoiceField(
        queryset=family.objects.all(),
        empty_label='Select a Family',
        label='Family',
    )
    subfamily = forms.ModelChoiceField(
                queryset=subfamily.objects.all(),
                empty_label='Select a Subfamily',
                label='Subfamily',
    )
    class Meta:
        model = product
        fields = ['product_name', 'product_size', 'color', 'product_price_sell', 'product_price_buy','product_reference', 'product_quantity' ]
        labels = {
            'product_name':'Name',
            'product_size': 'Size',
            'color': 'Color',
            'product_price_sell': 'Price Sell',
            'product_reference' : 'Ref',
            'product_price_buy' : 'Price Buy',
            'product_quantity' : 'Quantity',

            }
