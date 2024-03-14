from django import forms


class ConfigurationForm(forms.Form):
    """
    Formulario de configuración para cargar archivos .sh y .yaml.

    Este formulario permite al usuario cargar archivos con extensiones .sh y .yaml
    para su procesamiento posterior.

    Attributes:
        file_sh (forms.FileField): Campo para cargar archivos con extensión .sh.
        file_yaml (forms.FileField): Campo para cargar archivos con extensión .yaml.
    """
    file_sh = forms.FileField(label='Archivo .sh')
    file_yaml = forms.FileField(label='Archivo .yaml')

    def clean_file_sh(self):
        """
        Realiza validación sobre el archivo .sh cargado.

        Verifica que el archivo tenga la extensión .sh.

        Returns:
            El archivo .sh cargado si la validación es exitosa.

        Raises:
            forms.ValidationError: Si el archivo no tiene la extensión .sh.
        """
        file_sh = self.cleaned_data['file_sh']
        if not file_sh.name.endswith('.sh'):
            raise forms.ValidationError('El archivo debe tener extensión .sh')
        return file_sh

    def clean_file_yaml(self):
        """
        Realiza validación sobre el archivo .yaml cargado.

        Verifica que el archivo tenga la extensión .yaml.

        Returns:
            El archivo .yaml cargado si la validación es exitosa.

        Raises:
            forms.ValidationError: Si el archivo no tiene la extensión .yaml.
        """
        file_yaml = self.cleaned_data['file_yaml']
        if not file_yaml.name.endswith('.yaml'):
            raise forms.ValidationError(
                'El archivo debe tener extensión .yaml')
        return file_yaml
