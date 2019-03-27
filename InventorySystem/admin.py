from django.contrib import admin
from .models import UnitLookup, MaterialType, Material, Activity
# Register your models here.


admin.site.register(UnitLookup)
admin.site.register(MaterialType)
admin.site.register(Material)
admin.site.register(Activity)
