from .models import Material, MaterialType
from django.forms import ModelForm
from django import forms



class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {'material_type': forms.HiddenInput()}

class MaterialTypeForm(ModelForm):
    class Meta:
        model = MaterialType
        fields = '__all__'
        #widgets = {'date_updated': forms.HiddenInput()}
