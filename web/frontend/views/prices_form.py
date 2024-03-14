from django import forms
from django.conf import settings
import os

file_path = os.path.join(settings.BASE_DIR, 'files')


class PricesForm(forms.Form):
    """
    Formulario para ingresar precios de diferentes tipos de instancias.

    Este formulario genera campos para ingresar precios para cada tipo de instancia 
    definido en el archivo instance_types.txt ubicado en el directorio especificado 
    en la variable file_path.

    Attributes:
        file_path (str): Ruta al directorio que contiene el archivo instance_types.txt.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario y crea campos para cada tipo de instancia.

        Lee el archivo instance_types.txt ubicado en file_path para obtener los tipos de instancia.
        Por cada tipo de instancia encontrado, crea un campo FloatField en el formulario para 
        ingresar el precio correspondiente.

        Args:
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos de palabra clave adicionales.

        Raises:
            FileNotFoundError: Si no se encuentra el archivo instance_types.txt en file_path.
        """
        super().__init__(*args, **kwargs)
        instances_types = []
        with open(os.path.join(file_path, 'instance_types.txt'), "r") as f:
            instance_types = [line.strip() for line in f.readlines()]
        for instance_type in instance_types:
            self.fields[instance_type] = forms.FloatField(
                label='Precio instancia ' + instance_type, min_value=0)

    def clean(self):
        """
        Realiza validación adicional sobre los datos ingresados en el formulario.

        Valida que los valores ingresados para los precios de instancia no sean negativos.

        Returns:
            dict: Datos limpios después de la validación.

        Raises:
            forms.ValidationError: Si algún valor de precio es negativo.
        """
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if value is not None and value < 0:
                raise forms.ValidationError(
                    f"El valor de {field_name} no puede ser negativo.")
        return cleaned_data
