from django.urls import path
from cost_app import views


urlpatterns = [
    path('couts/', views.cost, name='cost'),
    path('couts/add-category-<str:calcul_mode>/', views.add_cost_category),
    path('couts/mod-category-<int:category_id>/', views.update_category_cost),
    path('couts/add-cout-<int:category_id>/', views.add_cost),
    path('couts/mod-cout-<int:cost_id>/', views.update_cost),
    path('couts/calcul/', views.calcul, name='calcul'),
    path(
        'couts/calcul/ajouter-couts-generaux/<int:cost_id>/',
        views.add_genaral_cost),
    path(
        'couts/calcul/couts-par-produit/<int:product_id>/',
        views.costs_per_product),
    path(
        'couts/calcul/ajouter-couts-par-produit/cost<int:cost_id>/product<int:product_id>/',
        views.add_cost_per_product),
    path(
        'couts/calcul/ajouter-couts-par-produit/<int:cost_id>/',
        views.add_cost_product),
    path(
        'couts/calcul/cout-produits/<int:cost_id>/',
        views.cost_products),
]
