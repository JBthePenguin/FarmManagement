from django.urls import path
from cost_app import views


urlpatterns = [
    path('couts/', views.cost, name='cost'),
    path('couts/add-category-<str:calcul_mode>/', views.add_cost_category),
    path('couts/mod-category-<int:category_id>/', views.update_category_cost),
]
