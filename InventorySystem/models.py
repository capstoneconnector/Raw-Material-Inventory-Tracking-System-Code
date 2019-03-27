from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''models.py includes models that structure the relational database.'''


'''
UnitLookup is used to make objects that represent units 
of measurement for Materials.
'''
class UnitLookup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

'''
MaterialType is used to make objects categorizing Materials into
a collection. (e.g. Bacon, Lamb, Beef, etc.) These MaterialTypes
are defined by a name, unit of measurement, a user ID for who previously
updated a Material of its type, and a date updated for when the changes 
by the user were made. 
'''
class MaterialType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    unit = models.ForeignKey(UnitLookup, on_delete=models.CASCADE, related_name='nit')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date_updated = models.DateField(null=True)

    def __str__(self):
        return self.name
    def as_json(self):
        return dict(
            material_type_name=self.name)

'''
Material is used to make objects that are Inventory of a Material Type.
A Material is defined with an initial amount, a current amount, a prepared
amount, an expiration date for the Material, and the material type it falls
under.
'''
class Material(models.Model):
    id = models.AutoField(primary_key=True)
    initial_amount = models.DecimalField(max_digits=6, decimal_places=2)
    current_amount = models.DecimalField(max_digits=6, decimal_places=2)
    prepared_amount = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)

    def as_json(self):
        return dict(
            id=self.id,
            material_type=self.material_type.name,
            current_amount=self.current_amount,
            buy_unit=self.material_type.buy_unit.name)


'''
The Activity model creates objects that describe user activity.
An Activity is defined by a current date (the date of when the 
activity was performed, a user who performed the activity, 
material type the activity effected, the action made, and 
a stock code (describing the specific Material in a Material Type
that is being edited). 
'''
class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    current_date = models.DateField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    stock_code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.material_type) + " " + str(self.action) + " by " + str(self.user) + " [ " + str(self.current_date) + " ] "
