from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Material, MaterialType
from .forms import MaterialForm, MaterialTypeForm
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta



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
        material_obj = {'name': material_type.name}
        material_obj['id'] = material_type.id
        total_amount = 0
        prepared_amount = 0
        total_initial_amount = 0
        used_amount = 0

        if len(Material.objects.filter(material_type=material_type)) == 0:
            material_obj['total_amount'] = 0
            material_obj['prepared_amount'] = 0
            material_obj['used_amount'] = 0
            material_obj['buy_unit'] = material_type.buy_unit
            materials.append(material_obj)
            continue

        earliest_expiration_material = Material.objects.filter(material_type=material_type).latest('-expiration_date')
        expiration_date = earliest_expiration_material.expiration_date
        material_obj['expiration_date'] = expiration_date

        for material in Material.objects.filter(material_type=material_type):
            total_amount += material.current_amount
            prepared_amount += material.prepared_amount
            total_initial_amount += material.initial_amount

        used_amount = total_initial_amount - total_amount

        material_obj['total_amount'] = total_amount
        material_obj['prepared_amount'] = prepared_amount
        material_obj['used_amount'] = used_amount
        material_obj['buy_unit'] = material_type.buy_unit.name
        materials.append(material_obj)

    return render(request, 'total_amount.html', {'materials': materials, 'form': {'mat': {'id': 0}, 'form': MaterialTypeForm()}})


def mat_instance_summary(request, materialName):
    material_type = MaterialType.objects.get(name=materialName)
    materials = Material.objects.filter(material_type=material_type)

    forms = []
    for mat in materials:
        form_data = {'mat': mat, 'form': MaterialForm(instance=mat)}
        forms.append(form_data)
    f = MaterialForm(initial={'material_type': material_type, 'updated_by':request.user.username})
    forms.append({'mat': {'id': 0}, 'form': f})

    return render(request, 'material_instance_summary.html', {'forms': forms, 'title': materialName, 'material_type': material_type.id})



@csrf_exempt
def material_instance(request, mat_id):
    if mat_id is not 0:
        material_obj = Material.objects.get(id=mat_id)
        f = MaterialForm(request.POST, instance=material_obj)
        f.save()
        print("You've successfuly made a change!")
        return HttpResponse("You've successfully updated an instance!")
        #redirect_url = 'material/summary/' + str(material_obj.material_type)
        #return redirect('/is/material/summary/' + str(material_obj.material_type))
    else:
        print(request.POST)
        f = MaterialForm(request.POST)
        f.save()
        #notification_days = int(f.data.get('notification_days'))
        #notification_date = datetime.strptime(f.data.get('expiration_date'), '%Y-%m-%d') - timedelta(days=notification_days)
        return HttpResponse("You've successfully added an instance!")

    return HttpResponse("Hey! You didn't give me any data!")

@csrf_exempt
def add_material_type(request, mat_type_id):
    if mat_type_id is not 0:
        '''material_type_obj = MaterialType.objects.get(id=mat_type_id)
        f = MaterialTypeForm(request.POST, instance=material_type_obj)
        f.save()'''
        return HttpResponse("Aye there's definitely something here already")
    else:
        print(request.POST)
        f = MaterialTypeForm(request.POST)
        f.save()
        return HttpResponse("Aye there's definitely something here now")

@csrf_exempt
def remove_material_instance(request, mat_id):
    try:
      Material.objects.get(id=mat_id).delete()
      return HttpResponse('Object deleted!')
    except Material.DoesNotExist:
      return HttpResponse('No object with that id!')


@csrf_exempt
def remove_material_type(request, mat_type_id):
    try:
        MaterialType.objects.get(id=mat_type_id).delete()
        return HttpResponse("Object Deleted!")
    except MaterialType.DoesNotExist:
        return HttpResponse('No object with that id!')
