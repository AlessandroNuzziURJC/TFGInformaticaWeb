from django import forms

class ConfigurationForm(forms.Form):
    file_sh = forms.FileField(label='Archivo .sh')
    file_yaml = forms.FileField(label='Archivo .yaml')

    def clean_file_sh(self):
        file_sh = self.cleaned_data['file_sh']
        if not file_sh.name.endswith('.sh'):
            raise forms.ValidationError('El archivo debe tener extensión .sh')
        return file_sh

    def clean_file_yaml(self):
        file_yaml = self.cleaned_data['file_yaml']
        if not file_yaml.name.endswith('.yaml'):
            raise forms.ValidationError('El archivo debe tener extensión .yaml')
        return file_yaml
