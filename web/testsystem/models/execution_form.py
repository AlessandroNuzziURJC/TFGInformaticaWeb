from django import forms
from testsystem.models.connection import Openstack_Service

class InfoForm(forms.Form):
    name = forms.CharField(max_length=100)
    instance_type = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reps = forms.IntegerField(min_value=0, max_value=100)
    email = forms.EmailField()
    lib = forms.MultipleChoiceField(
        choices=[('OpenMP', 'OpenMP'), ('MPI', 'MPI'), ('Ninguno', 'Ninguno')],
        widget=forms.CheckboxSelectMultiple, required=True
    )
    program = forms.FileField()
    vcpu = 0

    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        connection = Openstack_Service()
        connection.connect()
        instance_types_list = connection.instances_available()
        self.setup_instancia_choices(instance_types_list)
        self.vcpu = connection.free_vcpus()
        connection.disconnect()

    def setup_instancia_choices(self, instance_types_list):
        self.fields['instance_type'].choices = self.generate_instance_values(instance_types_list)

    def generate_instance_values(self, l):
        aux = []
        for e in l:
            aux.append((e, e))

        return aux
