from django.shortcuts import render, redirect
from django.http import JsonResponse
from testsystem.views.execution_form import InfoForm
from testsystem.models.execution_controller import ExecutionController
from testsystem.models.execution import Execution

import os
from django.conf import settings

execution_controller = ExecutionController()

def index_post(request):
    form = InfoForm(request.POST, request.FILES)
    if form.is_valid():
        execution = Execution(form.cleaned_data, request.FILES['program'])
        execution_controller.add(execution)
        return redirect('/testsystem/executions/')
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
    aux = list(execution_controller.queue)
    return render(request, 'index.html', {'executions': aux})


def queue(request):
    aux = list(execution_controller.queue)
    rendered_queue = render(request, 'queue.html', {'executions': aux})
    return JsonResponse({'executions': rendered_queue.content.decode()}, content_type='text/html')


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

