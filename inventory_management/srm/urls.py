from django.urls import path
from . import views 

app_name = 'srm'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('supplier_list/', views.supplier_list, name='supplier_list'),




]