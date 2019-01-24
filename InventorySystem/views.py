from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Material, MaterialType

# Create your views here.


def index(request):
    return HttpResponse('<h1>Inventory System Home!</h1>')


def material_instances(request, materialName):
    material_type = MaterialType.objects.get(name=materialName)
    results = [material_instance.as_json() for material_instance in Material.objects.filter(material_type = material_type)]
    return HttpResponse(results)


def material_total_amount(request,materialName):
    material_type = MaterialType.objects.get(name=materialName)
    material_buy_unit = material_type.buy_unit.name
    amount = 0
    for material in Material.objects.filter(material_type=material_type):
        amount += material.current_amount
    return JsonResponse({'name': materialName, 'total_amount': amount, 'unit': material_buy_unit})


def total_amounts(request):
    materials = []

    for material_type in MaterialType.objects.all():
        material_obj = {}
        material_obj['name'] = material_type.name

        amount = 0
        for material in Material.objects.filter(material_type=material_type):
            amount += material.current_amount

        material_obj['amount'] = amount
        material_obj['buy_unit'] = material_type.buy_unit.name
        materials.append(material_obj)


    return JsonResponse({'materials': materials})
