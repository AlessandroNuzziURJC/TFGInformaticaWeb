from django import forms
import os
from django.conf import settings

class InfoForm(forms.Form):
    exec_name = forms.CharField(max_length=100)
    reps = forms.IntegerField(min_value=1, max_value=100)
    email = forms.EmailField()
    program = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        instance_types_file = os.path.join(settings.BASE_DIR, 'files', 'instance_types.txt')  # Ruta al archivo de texto
        
        # Lee los tipos de instancia desde el archivo de texto y los convierte en una lista de tuplas
        with open(instance_types_file, "r") as f:
            instance_choices = [(line.strip(), line.strip()) for line in f.readlines()]

        self.fields['instance_types'] = forms.MultipleChoiceField(
            choices=instance_choices,
            widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_instance_types'})
        )
