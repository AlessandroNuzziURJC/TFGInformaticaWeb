from django.shortcuts import render, redirect
import requests
from django.urls import reverse
import shutil
from django.http import HttpResponse
from django.http import JsonResponse

from frontend.models.execution import Execution
from frontend.models.executions_info import ExecutionsInfo
from frontend.models.zip_generator import ZipGenerator
from frontend.models.data_extractor import DataExtractor

def executions(request):
    """
    Rellena el template executions.html con las ejecuciones.

    Args:
        request: HTTP Request.

    Returns:
        Devuelve un HttpResponse con la pagina HTML.
    """

    return render(request, 'executions.html')

def cards_list(request):
    executions = ExecutionsInfo()
    total_cards = executions.get_executions_info()

    relative_url = reverse('get_queue')
    absolute_url = request.build_absolute_uri(relative_url)
    response = requests.get(absolute_url)
    queue = response.json()
    cards = []
    for e in total_cards:
        found = False
        for queue_item in queue['queue']:
            if queue_item['execution_unique_name'] == e['execution_unique_name']:
                found = True
                break
        if not found:
            cards.append(e)

    context = {'cards': cards}
    rendered_cards= render(request, 'executions_cards.html', context)
    cards_html = rendered_cards.content.decode()
    return JsonResponse({'cards': cards_html, 'card_number': len(cards)}, content_type='text/html')

def delete_execution(request, execution_unique_name):
    """
        Elimina los datos de la ejecucion.

    Args:

    Returns:

    """
    path = './output/' + str(execution_unique_name)

    try:
        shutil.rmtree(path)
        print(f'Directorio {execution_unique_name} eliminado correctamente.')
    except FileNotFoundError:
        print(f'Directorio {execution_unique_name} no encontrado.')
    except OSError as e:
        print(f'Error al eliminar el directorio {execution_unique_name}: {e}')
    return redirect('/p3co/executions/')

def execution(request, execution_unique_name):
    """
    Rellena el template execution.html con los datos de la ejecucion correspondiente.

    Args:
        request: HTTP Request.
        execution_unique_name: identificador de la ejecucion.

    Returns:
        Devuelve un HttpResponse con la pagina HTML.
    """
    execution = Execution(execution_unique_name=execution_unique_name)
    output = execution.get_execution_info()
    return render(request, 'execution.html', output)


def datafiles(request, execution_unique_name):
    """
    Genera un ZIP con los datos generados en la ejecuciion indicada.

    Args:
        request: HTTP Request.
        execution_unique_name: identificador de la ejecucion.

    Returns:
        Devuelve un HttpResponse con el ZIP.
    """
    generator = ZipGenerator(execution_unique_name)
    output = generator.generate()

    response = HttpResponse(output['file'], content_type='application/zip')
    zip_name = output['nombre_zip']
    response['Content-Disposition'] = f'attachment; filename="{zip_name}"'
    return response

def data_times(request, execution_unique_name):
    """
    Devuelve los datos de una ejecucion para generar la grafica de tiempos en Javascript.

    Args:
        request: HTTP Request.
        execution_unique_name: identificador de la ejecucion.

    Returns:
        Devuelve un JsonResponse con los datos o una excepcion si algo no va bien.
    """
    try:
        extractor = DataExtractor(execution_unique_name)
        response_data = extractor.extract_times()
        return JsonResponse(response_data)
    except FileNotFoundError:
        return JsonResponse({'error': 'El archivo no se encontró'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def data_costs(request, execution_unique_name):
    """
    Devuelve los datos de una ejecucion para generar la grafica de costes en Javascript.

    Args:
        request: HTTP Request.
        execution_unique_name: identificador de la ejecucion.

    Returns:
        Devuelve un JsonResponse con los datos o una excepcion si algo no va bien.
    """
    try:
        extractor = DataExtractor(execution_unique_name)
        response_data = extractor.extract_cost()
        return JsonResponse(response_data)
    except FileNotFoundError:
        return JsonResponse({'error': 'El archivo no se encontró'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)