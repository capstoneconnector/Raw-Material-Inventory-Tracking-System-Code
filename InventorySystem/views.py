from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Material, MaterialType, Activity
from .forms import MaterialForm, MaterialTypeForm
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect



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
            material_obj['unit'] = material_type.unit
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
        material_obj['unit'] = material_type.unit.name
        material_obj['updated_by'] = material_type.updated_by
        material_obj['date_updated'] = material_type.date_updated.strftime('%Y-%m-%d')
        materials.append(material_obj)

    form_data = {'mat': {'id':0}, 'form': MaterialTypeForm(initial= {'updated_by': request.user, 'date_updated':timezone.now()})}

    return render(request, 'total_amount.html', {'materials': materials, 'form': form_data})

def mat_instance_summary(request, materialName, message):
    material_type = MaterialType.objects.get(name=materialName)
    materials = Material.objects.filter(material_type=material_type)
    message = message
    forms = []
    for mat in materials:
        form_data = {'mat': mat, 'form': MaterialForm(instance=mat)}
        forms.append(form_data)
    f = MaterialForm(initial={'material_type': material_type, 'updated_by': request.user.username})
    forms.append({'mat': {'id': 0}, 'form': f})

    return render(request, 'material_instance_summary.html', {'forms': forms, 'title': materialName,
                                                              'material_type': material_type.id, 'message': message})
@csrf_exempt
def material_instance(request, mat_id):
    message = ""
    if mat_id is not 0:
        try:
            material_obj = Material.objects.get(id=mat_id)
            f = MaterialForm(request.POST, instance=material_obj)
            f.save()

            material_type_obj = MaterialType.objects.get(id=material_obj.material_type.id)
            material_type_obj.updated_by = request.user
            material_type_obj.date_updated = timezone.now()

            add_activity(material_type_obj.name, "INVENTORY UPDATED", request.user, mat_id)
            message = str(mat_id) + " Updated"

            return mat_instance_summary(request, material_type_obj.name, message)
        
        except ValueError:
            return HttpResponse("Invalid Input")

        #redirect_url = 'material/summary/' + str(material_obj.material_type)
        #return redirect('/is/material/summary/' + str(material_obj.material_type))
    else:

        try:
            f = MaterialForm(request.POST)
            f.save()
            material_type_obj = MaterialType.objects.get(id=f.data.get('material_type'))
            material_type_obj.updated_by = request.user
            material_type_obj.date_updated = timezone.now()

            material_name = material_type_obj.name
            #notification_days = int(f.data.get('notification_days'))
            #notification_date = datetime.strptime(f.data.get('expiration_date'), '%Y-%m-%d') - timedelta(days=notification_days)

            mat_instance_id = Material.objects.last()
            add_activity(material_name, "INVENTORY ADDED", request.user, mat_instance_id.id)

            message = str(mat_instance_id.id) + " Added"

            return mat_instance_summary(request, material_type_obj.name, message)


            print("You've successfully added an instance!")
        except ValueError:
            return HttpResponse("Invalid Input")

    return HttpResponse("Hey! You didn't give me any data!")
@csrf_exempt
def remove_material_instance(request, mat_id):
    try:
      material = Material.objects.get(id=mat_id)
      material_type = material.material_type.name
      material.delete()
      print('Object deleted!')

      add_activity(material_type, "INVENTORY REMOVED", request.user, mat_id)

      return redirect('/is/material/summary/' + material_type)

    except Material.DoesNotExist:
      return HttpResponse('No object with that id!')

@csrf_exempt
def add_material_type(request, mat_type_id):
    if mat_type_id is not 0:
        '''material_type_obj = MaterialType.objects.get(id=mat_type_id)
        f = MaterialTypeForm(request.POST, instance=material_type_obj)
        f.save()'''
        return HttpResponse("Aye there's definitely something here already")
    else:
        print(request.POST)
        print(timezone.now())
        f = MaterialTypeForm(request.POST)
        mat_type_name = f.data.get('name')
        f.save()

        add_activity(mat_type_name, "TRACKED MATERIAL ADDED", request.user, None)

        return redirect('/is/material/')
        print("Aye there's definitely something here now")
@csrf_exempt
def remove_material_type(request, mat_type_id):
    try:
        mat = MaterialType.objects.get(id=mat_type_id)
        mat_name = mat.name
        MaterialType.objects.get(id=mat_type_id).delete()
        print("object deleted!")

        add_activity(mat_name, "TRACKED MATERIAL REMOVED", request.user, None)

        return redirect('/is/material')

    except MaterialType.DoesNotExist:
        return HttpResponse('No object with that id!')

def activity_summary(request):

    return render(request, 'activity_page.html', {'activities':Activity.objects.all().order_by("-id")})
@csrf_exempt
def add_activity(material_type, action, user, instance_id):

    if instance_id != 0:
        activity = Activity.objects.create(current_date=timezone.now(), user=user, material_type=material_type, action=action, stock_code=instance_id)
    else:
        activity = Activity.objects.create(current_date=timezone.now(), user=user, material_type=material_type, action=action)