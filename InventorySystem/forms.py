from .models import Material, MaterialType
from django.forms import ModelForm


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialTypeForm(ModelForm):
    class Meta:
        model = MaterialType
        fields = '__all__'
