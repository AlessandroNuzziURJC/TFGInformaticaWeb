from django import forms
import os
from django.conf import settings


class InfoForm(forms.Form):
    """
    Formulario de información para la creación de ejecuciones.

    Este formulario permite a los usuarios ingresar información necesaria para crear una ejecución,
    incluyendo el nombre de la ejecución, el número de repeticiones, la dirección de correo electrónico
    y el archivo del programa a ejecutar. Además, lee los tipos de instancia disponibles desde un archivo
    de texto y los muestra como opciones para que el usuario pueda seleccionar múltiples tipos de instancia.

    Attributes:
        exec_name (forms.CharField): Campo para ingresar el nombre de la ejecución (máximo 100 caracteres).
        reps (forms.IntegerField): Campo para ingresar el número de repeticiones (entre 1 y 100).
        email (forms.EmailField): Campo para ingresar la dirección de correo electrónico.
        program (forms.FileField): Campo para adjuntar el archivo del programa a ejecutar.
        instance_types (forms.MultipleChoiceField): Campo para seleccionar los tipos de instancia disponibles.
    """

    exec_name = forms.CharField(max_length=100)
    reps = forms.IntegerField(min_value=1, max_value=100)
    email = forms.EmailField()
    program = forms.FileField()

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario y agrega el campo instance_types.

        Lee los tipos de instancia desde un archivo de texto y los agrega como opciones al campo instance_types.

        Args:
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos de palabra clave adicionales.
        """
        super().__init__(*args, **kwargs)

        instance_types_file = os.path.join(
            settings.BASE_DIR, 'files', 'instance_types.txt')

        with open(instance_types_file, "r") as f:
            instance_choices = [(line.strip(), line.strip())
                                for line in f.readlines()]

        self.fields['instance_types'] = forms.MultipleChoiceField(
            choices=instance_choices,
            widget=forms.CheckboxSelectMultiple(
                attrs={'id': 'id_instance_types'})
        )
