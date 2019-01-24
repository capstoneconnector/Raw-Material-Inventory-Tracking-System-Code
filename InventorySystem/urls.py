from django.urls import path
from .views import index, material_instances, total_amounts, material_total_amount

urlpatterns = [
    path('', index),
    path('material/instances/<str:materialName>', material_instances),
    path('material/total/<str:materialName>', material_total_amount),
    path('material/', total_amounts)
]