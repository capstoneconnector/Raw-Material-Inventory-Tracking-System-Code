from django.urls import path
from .views import index, material_instances, total_amounts, material_total_amount, summary, material_instance, remove_material_instance

urlpatterns = [
    path('', index),
    path('material/instances/<str:materialName>', material_instances),
    path('material/total/<str:materialName>', material_total_amount),
    path('material/', total_amounts),
    path('material/summary/<str:materialName>', summary),
    path('material/update/<int:mat_id>', material_instance),
    path('material/delete/<int:mat_id>', remove_material_instance)
]