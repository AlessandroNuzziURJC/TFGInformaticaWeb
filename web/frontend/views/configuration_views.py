import shutil
from django.shortcuts import render, redirect
from django.http import HttpResponse
from frontend.views.configuration_form import ConfigurationForm
from frontend.views.prices_form import PricesForm
from django.urls import reverse
from django.conf import settings
import os
import requests

file_path = os.path.join(settings.BASE_DIR, 'files')


def configuration(request):
    """
    Muestra el formulario de configuración y los archivos existentes.

    Si la solicitud es POST, procesa el formulario y los archivos cargados.
    Si no existen los directorios y archivos necesarios, los crea.
    Comprueba la existencia de archivos de configuración y devuelve su estado.

    Args:
        request: Objeto HttpRequest.

    Returns:
        HttpResponse con la página HTML renderizada.
    """
    if request.method == 'POST':
        return configuration_post(request)
    form = ConfigurationForm()
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    if not os.path.exists(file_path + '/instance_types.txt'):
        prices_form_exist = False
        prices_form = None
    else:
        prices_form_exist = True
        prices_form = PricesForm()

    yaml = False
    sh = False
    yaml_file = None
    sh_file = None

    relative_url = reverse('exists_conf_files')
    absolute_url = request.build_absolute_uri(relative_url)
    response = requests.get(absolute_url)
    if response.status_code == 200:
        data = response.json()
        yaml_file_name = data.get('yaml_file_name')
        sh_file_name = data.get('sh_file_name')

        if yaml_file_name is not None:
            yaml = True
            yaml_file = yaml_file_name

        if sh_file_name is not None:
            sh = True
            sh_file = sh_file_name

    return render(request, 'configuration.html', {'form': form,
                                                  'prices_exist': exists_price_file(),
                                                  'prices_form_exist': prices_form_exist,
                                                  'prices_form': prices_form,
                                                  'yaml_file_exists': yaml,
                                                  'script_file_exists': sh,
                                                  'yaml_file': yaml_file,
                                                  'sh_file': sh_file})


def configuration_post(request):
    """
    Procesa el formulario de configuración enviado por el usuario.

    Si el formulario es válido, carga los archivos .sh y .yaml y los envía al servicio api.
    Si el formulario de precios es válido, guarda los datos en un archivo prices.txt.

    Args:
        request: Objeto HttpRequest.

    Returns:
        Redirecciona a la página de configuración.
    """
    form = ConfigurationForm(request.POST, request.FILES)
    if form.is_valid():
        file_sh = request.FILES['file_sh']
        file_yaml = request.FILES['file_yaml']

        # Crear una solicitud multipart/form-data
        files = {
            'file_sh': (file_sh.name, file_sh, file_sh.content_type),
            'file_yaml': (file_yaml.name, file_yaml, file_yaml.content_type)
        }

        relative_url = reverse('store_conf_files')
        absolute_url = request.build_absolute_uri(relative_url)
        requests.post(absolute_url, files=files)
    form = PricesForm(request.POST, request.FILES)

    if form.is_valid():
        ubication = os.path.join(
            settings.MEDIA_ROOT, file_path, 'prices.txt')
        if os.path.exists(ubication):
            os.remove(ubication)
        with open(ubication, 'w') as file:
            for key, value in form.cleaned_data.items():
                line = f"{key}: {value}\n"
                file.write(line)
    return redirect(reverse(configuration))


def price_file(request):
    """
    Descarga el archivo de precios (prices.txt) si existe.

    Args:
        request: Objeto HttpRequest.

    Returns:
        HttpResponse con el archivo prices.txt si existe, o None si no existe.
    """
    response = None
    with open(os.path.join(file_path, 'prices.txt'), 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/txt')
        response['Content-Disposition'] = f'attachment; filename=prices.txt'
    return response


def exists_price_file():
    """
    Comprueba si existe un archivo de precios (prices.txt).

    Returns:
        True si existe un archivo de precios, False de lo contrario.
    """
    for file_name in os.listdir(file_path):
        if file_name == 'prices.txt':
            return True

    return False
