from django.contrib import admin
from django.urls import path, include
from .views import index, material_instances, total_amounts, material_total_amount, mat_instance_summary, material_instance, remove_material_instance, \
    add_material_type,remove_material_type, activity_summary


urlpatterns = [

    path('', index),

    # Shows all instances of a certain material
    path('material/instances/<str:materialName>', material_instances),

    # Calls the material total amount of the given material,
    # gets the total amount of all instances of that material type.
    path('material/total/<str:materialName>', material_total_amount),

    # Material takes you to the main summary page, in which you can see the materials being tracked,
    # information about them,the user who last updated that information, and options to add or remove
    # materials.
    path('material/', total_amounts),

    # Pulls up the material summary page of a specific material selected by the user
    path('material/summary/<str:materialName>', mat_instance_summary),

    # Updates the information of an instance of a material
    path('material/update/<int:mat_id>', material_instance),

    # Removes an instance of a material
    path('material/delete/<int:mat_id>', remove_material_instance),

    # Adds a new material to track
    path('material/type/update/<int:mat_type_id>', add_material_type),

    # Removes a type of material from the summary
    path('material/type/remove/<int:mat_type_id>', remove_material_type),

    # Activity brings the user to the activity page, which shows recent actions taken by users, such as
    # adding or removing materials, as well as the dates these changes were made
    path('activity', activity_summary),



]