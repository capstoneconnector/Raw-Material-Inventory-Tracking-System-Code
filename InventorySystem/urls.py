from django.contrib import admin
from django.urls import path, include
from .views import index, material_instances, total_amounts, material_total_amount, mat_instance_summary, material_instance, remove_material_instance, add_material_type,remove_material_type


urlpatterns = [

    path('', index),
    path('material/instances/<str:materialName>', material_instances),
    path('material/total/<str:materialName>', material_total_amount),
    path('material/', total_amounts),
    path('material/summary/<str:materialName>', mat_instance_summary),
    path('material/update/<int:mat_id>', material_instance),
    path('material/delete/<int:mat_id>', remove_material_instance),
    path('material/type/update/<int:mat_type_id>', add_material_type),
    path('material/type/remove/<int:mat_type_id>', remove_material_type),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),



]