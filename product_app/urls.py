from django.urls import path
from product_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('produits/', views.product, name='product'),
    path('produits/<int:product_id>/', views.update_product)
]
