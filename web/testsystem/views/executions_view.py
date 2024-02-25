from django.shortcuts import render
from testsystem.models.executions_info import ExecutionsInfo

def executions(request):
    """
    Rellena el template executions.html con las ejecuciones.

    Args:
        request: HTTP Request.

    Returns:
        Devuelve un HttpResponse con la pagina HTML.
    """
    executions = ExecutionsInfo()
    tarjetas = executions.get_executions_info()
    context = {'tarjetas': tarjetas}
    return render(request, 'executions.html', context)