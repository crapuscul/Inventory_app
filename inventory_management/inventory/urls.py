
# inventory/urls.py
from django.urls import path
from . import views


app_name = 'inventory'
urlpatterns = [
    path('', views.index, name='index'),


    path('family_list/', views.family_list, name='family_list'),
    path('subfamily_list/', views.subfamily_list, name='subfamily_list'),
    path('add_subfamily/', views.add_subfamily, name='add_subfamily'),
    path('subfamily/edit/<int:pk>/', views.edit_subfamily, name='edit_subfamily'),
    path('subfamily/delete/<int:pk>', views.delete_subfamily, name='delete_subfamily'),
    path('add_family/', views.add_family, name= 'add_family'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('generate_label/<int:pk>/', views.generate_label, name='generate_label'),
    path('products/<int:pk>/print_label/', views.print_label, name='print_label'),

]

