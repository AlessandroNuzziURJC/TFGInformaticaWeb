from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from testsystem.views.execution_form import InfoForm
from testsystem.models.execution_controller import ExecutionController
from testsystem.models.execution import Execution

import requests
import os
from django.conf import settings

execution_controller = ExecutionController()

def index_post(request):
    form = InfoForm(request.POST, request.FILES)
    if form.is_valid():
        program_file = request.FILES['program']
        execution = Execution(form.cleaned_data, program_file)
        
        # Construir los datos de la solicitud multipart/form-data
        data = {
            'exec_name': execution.exec_name,
            'reps': execution.reps,
            'email': execution.email,
            'OpenMP': execution.OpenMP,
            'MPI': execution.MPI,
        }
        archivo_bytes = b''
        for chunk in program_file.chunks():
            archivo_bytes += chunk
        files = {'program': (program_file.name, archivo_bytes, program_file.content_type)}
        relative_url = reverse('enqueue')
        absolute_url = request.build_absolute_uri(relative_url)
        response = requests.post(absolute_url, data=data, files=files)

        if response.status_code == 200:
            return redirect('/testsystem/index/')
        else:
            return redirect('/testsystem/index/')
    else:
        return redirect('/testsystem/index/')


def index(request):
    """
    Rellena el template inicio.html con el formulario.

    Args:
        request: HTTP Request.

    Returns:
        Devuelve un HttpResponse con la pagina HTML.
    """
    if request.method == 'POST':
        return index_post(request)
    return render(request, 'index.html', {'executions': []})


def form(request):
    if not verified_user():
        rendered_form = render(request, 'user_not_found_form.html') 
        form_html = rendered_form.content.decode()
        return JsonResponse({'form': form_html}, content_type='text/html')
    form = InfoForm()
    rendered_form = render(request, 'form.html', {'form': form})
    form_html = rendered_form.content.decode()
    return JsonResponse({'form': form_html}, content_type='text/html')

def verified_user():
    file_path = os.path.join(settings.BASE_DIR, 'testsystem/files/user_data.txt')
    return os.path.exists(file_path)

