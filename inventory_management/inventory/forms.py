# inventory/forms.py
from django import forms
from .models import product, family, subfamily
from srm.models import supplier



class FamilyForm(forms.ModelForm):
    class Meta:
        model = family
        fields = ['family_name']
        labels = {
            'family_name': 'Family Name',
        }
        widgets = {
            'family_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubFamilyForm(forms.ModelForm):
    class Meta:
        model = subfamily
        fields = ['subfamily_name']
        labels = {
            'subfamily_name': 'Subfamily Name',
            'family': 'Family',
        }
        widgets = {
            'subfamily_name': forms.TextInput(attrs={'class': 'form-control'}),
            'family': forms.Select(attrs={'class': 'form-control'}),
        }

    family = forms.ModelChoiceField(
        queryset=family.objects.all(),
        empty_label='Select a Family',
        label='Family',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

class SubFamilyEditForm(forms.ModelForm):
    class Meta:
        model= subfamily
        fields = ['subfamily_name','family']
        labels = {
            'subfamily_name': 'Subfamily Name',
            'family': 'Family',
        }
        widgets = {
            'subfamily_name': forms.TextInput(attrs={'class': 'form-control'}),
            'family': forms.Select(attrs={'class': 'form-control'}),
        }

    family = forms.ModelChoiceField(
            queryset=family.objects.all(),
            empty_label='Select a Family',
            label='Family',
            widget=forms.Select(attrs={'class': 'form-control'}),
    )

class ProductForm(forms.ModelForm):


    family = forms.ModelChoiceField(
            queryset=family.objects.all(),
            empty_label='Select a Category',
            label='family_name',
            widget= forms.Select(attrs={'class': 'form-control'}),
    )
    subfamily = forms.ModelChoiceField(
            queryset=subfamily.objects.all(),
            empty_label='Select a Sub-category',
            label='subfamily_name',
            widget= forms.Select(attrs={'class': 'form-control'}),
    )
    supplier = forms.ModelChoiceField(
            queryset=supplier.objects.all(),
            empty_label='Select a Supplier',
            label='supplier_name',
            widget= forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = product
        fields = ['product_name', 'product_price_sell', 'product_price_buy','product_reference', 'product_quantity' ]
        labels = {
            'product_name':'Name',
            'product_price_sell': 'Price Sell',
            'product_reference' : 'Ref',
            'product_price_buy' : 'Price Buy',
            'product_quantity' : 'Quantity',

            }
        widgets = {
            'product_name': forms.TextInput(attrs={'class':'form-control'}),
            #'product_size':  forms.TextInput(attrs={'class':'form-control'}),
            #'color':  forms.TextInput(attrs={'class':'form-control'}),
            'product_price_sell': forms.TextInput(attrs={'class':'form-control'}),
            'product_price_buy' : forms.TextInput(attrs={'class':'form-control'}),
            'product_reference' :forms.TextInput(attrs={'class':'form-control'}),
            'product_quantity' : forms.TextInput(attrs={'class':'form-control'}),
        }
