from django.urls import path
from basket_app import views


urlpatterns = [
    path('paniers/', views.basket, name='basket'),
    path(
        'paniers/add-category', views.add_category_basket,
        name='add_category_basket'),
    path('paniers/categorie<int:category_id>/', views.update_category_basket),
    path('paniers/creer-panier', views.create_basket, name='create_basket'),
    path('paniers/numero<int:basket_number>/', views.update_basket),
]
