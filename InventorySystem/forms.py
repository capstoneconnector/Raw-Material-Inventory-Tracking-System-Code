from .models import Material
from django.forms import ModelForm


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
