from django.urls import path
from client_app import views


urlpatterns = [
    path('clients/', views.client, name='client'),
    path('clients/add-category', views.add_category, name='add_category'),
    path('clients/categorie<int:category_id>/', views.update_category),
    path('clients/add-client', views.add_client, name='add_client'),
    path('clients/<int:client_id>/', views.update_client),
]
