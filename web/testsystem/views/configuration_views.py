import shutil
from django.shortcuts import render, redirect
from django.http import HttpResponse
from testsystem.views.configuration_form import ConfigurationForm
from django.urls import reverse
from django.conf import settings
import os
import requests

from testsystem.models.connection import Openstack_Service

file_path = os.path.join(settings.BASE_DIR, 'testsystem/files')


def configuration(request):
    if request.method == 'POST':
        return configuration_post(request)
    form = ConfigurationForm()
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    yaml = False
    sh = False
    yaml_file = None
    sh_file = None

    response = requests.get('http://localhost:8080/api/exists_yaml_conf_file/')
    if response.status_code == 200:
        data = response.json()
        yaml_file_name = data.get('name')
        
        if yaml_file_name is not None:
            yaml = True
            yaml_file = yaml_file_name

    response = requests.get('http://localhost:8080/api/exists_sh_conf_file/')
    if response.status_code == 200:
        data = response.json()
        sh_file_name = data.get('name')
        
        if sh_file_name is not None:
            sh = True
            sh_file = sh_file_name
    
    return render(request, 'configuration.html', {'form': form,
                                                  'yaml_file_exists': yaml,
                                                  'script_file_exists': sh,
                                                  'yaml_file': yaml_file,
                                                  'sh_file': sh_file})


def configuration_post(request):
    form = ConfigurationForm(request.POST, request.FILES)
    if form.is_valid():
        file_sh = request.FILES['file_sh']
        file_yaml = request.FILES['file_yaml']

        # Crear una solicitud multipart/form-data
        files = {
            'file_sh': (file_sh.name, file_sh, file_sh.content_type),
            'file_yaml': (file_yaml.name, file_yaml, file_yaml.content_type)
        }

        # Hacer una solicitud POST con los archivos
        response = requests.post('http://localhost:8080/api/store_conf_files/', files=files)
        if response.status_code == 200:
            if os.path.exists(file_path):
                shutil.rmtree(file_path)
            os.makedirs(file_path)
            
            ubication = os.path.join(
                settings.MEDIA_ROOT, file_path, file_sh.name)
            with open(ubication, 'wb') as file:
                for chunk in file_sh.chunks():
                    file.write(chunk)

            ubication = os.path.join(
                settings.MEDIA_ROOT, file_path, file_yaml.name)
            with open(ubication, 'wb') as file:
                for chunk in file_yaml.chunks():
                    file.write(chunk)

            generate_info_txt()
            os.remove(file_path + '/' + file_sh.name)
            os.remove(file_path + '/' + file_yaml.name)
            
    return redirect(reverse(configuration))


def generate_info_txt():
    openstack = Openstack_Service()
    openstack.connect()
    generate_file_user_data(openstack)
    generate_file_instance_type(openstack)
    openstack.disconnect()


def generate_file_user_data(openstack):
    path = os.path.join(
        settings.BASE_DIR, file_path, 'user_data.txt')
    with open(path, 'w') as file:
        limits = openstack.get_limits()
        for e in limits:
            file.write(e + ': ' + str(limits[e]) + '\n')


def generate_file_instance_type(openstack):
    path = os.path.join(
        settings.BASE_DIR, file_path, 'instance_types.txt')
    with open(path, 'w') as file:
        instances = openstack.instances_available()
        for e in instances:
            file.write(e + '\n')


def yaml_config_file(request):
    response = requests.get('http://localhost:8080/api/get_yaml_conf_file/')
    
    if response.status_code == 200:
        output =  HttpResponse(response.content, content_type=response.headers['Content-Type'])
        output['Content-Disposition'] = f'attachment; ' + response.headers.get('Content-Disposition')[response.headers.get('Content-Disposition').find('filename='):]
        return output
    
    return HttpResponse("Error: No se pudo obtener el archivo YAML", status=500)


def script_config_file(request):
    response = requests.get('http://localhost:8080/api/get_sh_conf_file/')
    
    if response.status_code == 200:
        output =  HttpResponse(response.content, content_type=response.headers['Content-Type'])
        output['Content-Disposition'] = f'attachment; ' + response.headers.get('Content-Disposition')[response.headers.get('Content-Disposition').find('filename='):]
        return output
    
    return HttpResponse("Error: No se pudo obtener el archivo sh", status=500)
