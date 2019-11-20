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
        views.add_genaral_cost)
]
