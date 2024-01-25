from django import forms
from .models import supplier 

class SupplierForm(forms.ModelForm):
    class Meta:
        model = supplier
        fields =['supplier_name', 'supplier_contact_name','supplier_city','supplier_phone',]
        labels = {
            'supplier_name':'Supplier Name',
            'supplier_contact_name': 'Contact Name',
            'supplier_city': 'City',
            'supplier_phone': 'Number',


        }
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_city': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_phone': forms.TextInput(attrs={'class': 'form-control'}),

        }