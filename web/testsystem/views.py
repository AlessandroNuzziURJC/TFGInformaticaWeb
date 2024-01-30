from django.shortcuts import render, redirect
from django.http import JsonResponse
from testsystem.models.execution_form import InfoForm
from testsystem.models.execution_controller import ExecutionController
from testsystem.models.execution import Execution

execution_controller = ExecutionController()

def configuration(request):
    return render(request, 'configuration.html')

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
    return render(request, 'index.html', {'executions' : aux})

def queue(request):
    aux = list(execution_controller.queue)
    rendered_queue = render(request, 'queue.html', {'executions': aux})
    return JsonResponse({'executions': rendered_queue.content.decode()}, content_type='text/html')


def form(request):
    form = InfoForm()
    rendered_form = render(request, 'form.html', {'form': form})
    form_html = rendered_form.content.decode()
    return JsonResponse({'form': form_html}, content_type='text/html')

def executions(request):
    """
    Rellena el template executions.html con las ejecuciones.

    Args:
        request: HTTP Request.

    Returns:
        Devuelve un HttpResponse con la pagina HTML.
    """
    #executions = ExecutionsInfo()
    #tarjetas = executions.get_executions_info()
    #context = {'tarjetas': tarjetas}
    return render(request, 'executions.html')