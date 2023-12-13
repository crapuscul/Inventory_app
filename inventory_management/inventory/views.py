from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

#index:
def index(request):
    return render(request,'inventory/index.html')


#Product_list:
def product_list(request):
    products = Product.objects.all()
    return render(request,'inventory/product_list.html', {'products': products})

#add_product:
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html',{'form':form} )

#edit_product:
def edit_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_product.html',{'form':form,'product': product})

#delete_product:

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('inventory:product_list')

    return render(request, 'inventory/delete_product.html', {'product': product})






# Create your views here.
