from django.urls import path
from product_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('produits/', views.product, name='product'),
    path('produits/add/', views.add_product, name='add_product'),
    path('produits/<int:product_id>/', views.update_product)
]
