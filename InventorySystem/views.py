from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Material, MaterialType
from .forms import MaterialForm
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

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


def summary(request, materialName):
    material_type = MaterialType.objects.get(name=materialName)
    materials = Material.objects.filter(material_type=material_type)

    forms = []
    for mat in materials:
        form_data = {'mat': mat, 'form': MaterialForm(instance=mat)}
        forms.append(form_data)
    f = MaterialForm(initial={'material_type': material_type})
    forms.append({'mat': {'id': 0}, 'form': f})

    return render(request, 'material_instance_summary.html', {'forms': forms, 'title': materialName, 'material_type': material_type.id})


@csrf_exempt
def material_instance(request, mat_id):
    if mat_id is not 0:
        material_obj = Material.objects.get(id=mat_id)
        f = MaterialForm(request.POST, instance=material_obj)
        f.save()
        return HttpResponse("You've successfuly made a change!")
    else:
        print(request.POST)
        f = MaterialForm(request.POST)
        f.save()
        return HttpResponse("You've successfully added an instance!")

    return HttpResponse("Hey! You didn't give me any data!")

@csrf_exempt
def remove_material_instance(request, mat_id):
  try:
      Material.objects.get(id=mat_id).delete()
      return HttpResponse('Object deleted!')
  except Material.DoesNotExist:
      return HttpResponse('No object with that id!')
