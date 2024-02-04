from django import forms

class InfoForm(forms.Form):
    name = forms.CharField(max_length=100)
    '''instance_type = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )'''
    reps = forms.IntegerField(min_value=0, max_value=100)
    email = forms.EmailField()
    lib = forms.MultipleChoiceField(
        choices=[('OpenMP', 'OpenMP'), ('MPI', 'MPI'), ('Ninguno', 'Ninguno')],
        widget=forms.CheckboxSelectMultiple, required=True
    )
    program = forms.FileField()
