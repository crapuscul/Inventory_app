from django.shortcuts import render, get_object_or_404, redirect
from .models import product, family, subfamily
from .forms import ProductForm, FamilyForm, SubFamilyForm, SubFamilyEditForm
#import logging
from django.http import HttpResponseBadRequest



#index:
def index(request):
    return render(request,'inventory/index.html')

#family_list:
def family_list(request):
    families = family.objects.all()
    return render(request,'inventory/family_list.html', {'families': families})

#subfamily_list
def subfamily_list(request):
    subfamilies = subfamily.objects.all()
    return render(request, 'inventory/subfamily_list.html', {'subfamilies': subfamilies})


#add_family:
def add_family(request):
    if request.method == 'POST':
        family_form = FamilyForm(request.POST)
        if family_form.is_valid():
            family_form.save()
            return redirect('inventory:family_list')
    else:
        family_form = FamilyForm()
    return render(request, 'inventory/add_family.html',{'family_form':family_form})

#logger = logging.getLogger(__name__)

def add_subfamily(request):
    if request.method == 'POST':
        subfamily_form = SubFamilyForm(request.POST, prefix='subfamily')
        #logger.error(request.POST)  # Logging line

        if subfamily_form.is_valid():
            subfamily_instance = subfamily_form.save(commit=False)

            # Get the family instance ID from the form data
            family_instance_id = request.POST.get('subfamily-family')
            #logger.error(f"Family instance ID: {family_instance_id}")  # Logging line

            if family_instance_id is None:
                return HttpResponseBadRequest("Missing 'subfamily-family' field in form data.")

            # Retrieve the corresponding family instance
            family_instance = get_object_or_404(family, pk=family_instance_id)

            subfamily_instance.family = family_instance
            subfamily_instance.save()
            return redirect('inventory:family_list')  # Redirect wherever appropriate

    else:
        subfamily_form = SubFamilyForm(prefix='subfamily')

    return render(request, 'inventory/add_subfamily.html', {'subfamily_form': subfamily_form})

#Product_list:
def product_list(request):
    products = product.objects.all()
    return render(request,'inventory/product_list.html', {'products': products})

#add_product:


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, prefix='product')
        family_form = FamilyForm(request.POST, prefix='family')
        subfamily_form = SubFamilyForm(request.POST, prefix='subfamily')
        if product_form.is_valid() and family_form.is_valid() and subfamily_form.is_valid():
            # Debugging statements
            print("All forms are valid")

            #save family_form and subfamily_form
            family_instance = family_form.save()
            print("Family instance saved:", family_instance)

            subfamily_instance = subfamily_form.save(commit=False) # saves the data from the subfamily_form but doesn't commit it to the database yet
            subfamily_instance.family = family_instance # establieshes a link between the 'subfamily' instance and the 'family' instance
            subfamily_instance.save()
            print("Subfamily instance saved:", subfamily_instance)
            #save the product with family and subfamily
            product_instance = product_form.save(commit=False) # saves the data from the product_form but doesnt commit it yet to the db. it returns an instance of the product model
            product_instance.family = family_instance #establieshs a link between the product and family instance because the product model has a FK refering to the family model
            product_instance.subfamily = subfamily_instance #establishes a link between the prodcut and subfamily instance, FK ref to the subfamily model
            product_instance.save()
            print("Product instance saved:", product_instance)

        else:
            # Debugging statements to identify form errors
            print("Form errors:")
            print("Product form errors:", product_form.errors)
            print("Family form errors:", family_form.errors)
            print("Subfamily form errors:", subfamily_form.errors)

         #   return redirect('inventory:index')  # Redirect wherever appropriate

    else:
        product_form = ProductForm(prefix='product')
        family_form = FamilyForm(prefix= 'family')
        subfamily_form = SubFamilyForm(prefix= 'subfamily')
    return render(request, 'inventory/add_product.html',{'product_form':product_form, 'family_form':family_form, 'subfamily_form':subfamily_form} )


#edit_subfamily:
def edit_subfamily(request, pk):
    subfamily_instance = get_object_or_404(subfamily, pk=pk)
    if request.method == 'POST':
        subfamily_form = SubFamilyEditForm(request.POST, instance=subfamily_instance)
        if subfamily_form.is_valid():
            subfamily_form.save()
            return redirect('inventory:subfamily_list')
    else:
        subfamily_form = SubFamilyEditForm(instance=subfamily_instance)
    return render(request, 'inventory/edit_subfamily.html',{'subfamily_form':subfamily_form,'subfamily_instance': subfamily_instance})


#delete_subfamily:
def delete_subfamily(request, pk):
    subfamily_instance = get_object_or_404(subfamily, pk=pk)

    if request.method == 'POST':
        subfamily_instance.delete()
        return redirect ('inventory:subfamily_list')

    return render(request, 'inventory/delete_subfamily.html', {'subfamily': subfamily_instance})


#edit_product:
def edit_product(request,pk):
    prod_instance = get_object_or_404(product, pk = pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=prod_instance)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=prod_instance)
    return render(request, 'inventory/edit_product.html',{'form':form,'product': prod_instance})

#delete_product:

def delete_product(request, pk):
    prod_instance = get_object_or_404(product, pk = pk)

    if request.method == 'POST':
        prod_instance.delete()
        return redirect('inventory:product_list')

    return render(request, 'inventory/delete_product.html', {'product': prod_instance})






# Create your views here.
