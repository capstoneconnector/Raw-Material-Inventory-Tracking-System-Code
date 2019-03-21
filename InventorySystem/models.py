from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class UnitLookup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class MaterialType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    buy_unit = models.ForeignKey(UnitLookup, on_delete=models.CASCADE, related_name='buy_unit')
    sell_unit = models.ForeignKey(UnitLookup, on_delete=models.CASCADE, related_name='sell_unit')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date_updated = models.DateField(null=True)
    '''buy_unit_cost = models.DecimalField(max_digits=6, decimal_places=2)'''
    '''sell_unit_cost = models.DecimalField(max_digits=6, decimal_places=2)'''

    def __str__(self):
        return self.name
    def as_json(self):
        return dict(
            material_type_name=self.name)


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

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    current_date = models.DateField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=50)
    action = models.CharField(max_length=50)

    def __str__(self):
        return str(self.material_type) + " " + str(self.action) + " by " + str(self.user) + " [ " + str(self.current_date) + " ] "
