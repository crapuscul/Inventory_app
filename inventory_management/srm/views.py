from django.shortcuts import render, get_object_or_404, redirect
from .models import supplier 
from .forms import SupplierForm

def index(request):
    return render(request, 'srm/index.html')

def supplier_list(request):
    suppliers = supplier.objects.all()
    return render(request, 'srm/supplier_list.html', {'suppliers': suppliers})


def add_supplier(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier_form.save()
            return redirect('srm:supplier_list')
    else:
        supplier_form = SupplierForm()
    return render(request, 'srm/add_supplier.html',{'supplier_form':supplier_form})    


# Create your views here.
