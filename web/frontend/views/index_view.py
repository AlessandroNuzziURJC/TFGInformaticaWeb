from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from frontend.views.execution_form import InfoForm
from frontend.models.execution import Execution
import requests
import os
from django.conf import settings


def index_post(request):
    """
    Procesa el formulario enviado desde la página de inicio.

    Si el formulario es válido, crea una instancia de Execution con los datos del formulario
    y el archivo adjunto, y envía una solicitud POST a la URL especificada para encolar
    la ejecución.

    Args:
        request: Objeto HttpRequest.

    Returns:
        Redirecciona a la página de inicio (/p3co/index/) si la solicitud es exitosa.
        Redirecciona a la página de inicio (/p3co/index/) si la solicitud falla.
    """
    form = InfoForm(request.POST, request.FILES)
    if form.is_valid():
        program_file = request.FILES['program']
        execution = Execution(form_data=form.cleaned_data, file=program_file)

        data = {
            'exec_name': execution.exec_name,
            'instance_types': execution.instance_types,
            'reps': execution.reps,
            'email': execution.email,
            'OpenMP': execution.OpenMP,
            'MPI': execution.MPI,
        }

        archivo_bytes = b''
        for chunk in program_file.chunks():
            archivo_bytes += chunk
        files = {'program': (program_file.name, archivo_bytes,
                             program_file.content_type)}
        relative_url = reverse('enqueue')
        absolute_url = request.build_absolute_uri(relative_url)
        response = requests.post(absolute_url, data=data, files=files)

        if response.status_code == 200:
            return redirect('/p3co/index/')
        else:
            return redirect('/p3co/index/')
    else:
        return redirect('/p3co/index/')


def index(request):
    """
    Renderiza la página de inicio con el formulario.

    Si la solicitud es POST, procesa el formulario.

    Args:
        request: Objeto HttpRequest.

    Returns:
        Un HttpResponse con la página HTML renderizada.
    """
    if request.method == 'POST':
        return index_post(request)
    return render(request, 'index.html', {'executions': []})


def form(request):
    """
    Retorna el formulario para la creación de ejecuciones.

    Si el usuario no está verificado, se renderiza un mesaje para que se aporten los archivos necesarios.

    Args:
        request: Objeto HttpRequest.

    Returns:
        JsonResponse con el contenido HTML del formulario o un mensaje de error si el usuario no está verificado.
    """
    rendered_form = None
    if not verified_user():
        rendered_form = render(request, 'user_not_found_form.html')
    else:
        form = InfoForm()
        rendered_form = render(request, 'form.html', {'form': form})
    form_html = rendered_form.content.decode()
    return JsonResponse({'form': form_html}, content_type='text/html')


def verified_user():
    """
    Verifica si el usuario está verificado.

    Verifica si existen los archivos de datos de usuario y de precios.

    Returns:
        True si el usuario está verificado, False de lo contrario.
    """
    file_path = os.path.join(settings.BASE_DIR, 'files/user_data.txt')
    prices_path = os.path.join(settings.BASE_DIR, 'files/prices.txt')
    return os.path.exists(file_path) and os.path.exists(prices_path)
