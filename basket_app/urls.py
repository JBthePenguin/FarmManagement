from django.urls import path
from basket_app import views


urlpatterns = [
    path('paniers/', views.basket, name='basket'),
]
