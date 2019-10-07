from django.urls import path
from order_app import views


urlpatterns = [
    path('commandes/', views.order, name='order'),
    path('commandes/creer-commande/', views.create_order, name='create_order'),
]
