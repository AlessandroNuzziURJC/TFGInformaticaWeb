from django import forms
from django.conf import settings
import os

file_path = os.path.join(settings.BASE_DIR, 'files')

class PricesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instances_types = []
        with open(os.path.join(file_path, 'instance_types.txt'), "r") as f:
            instance_types = [line.strip() for line in f.readlines()]
        for instance_type in instance_types:
            self.fields[instance_type] = forms.FloatField(label='Precio instancia ' + instance_type, min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if value is not None and value < 0:
                raise forms.ValidationError(f"El valor de {field_name} no puede ser negativo.")
        return cleaned_data
