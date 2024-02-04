import shutil
from django.shortcuts import render, redirect
from django.http import HttpResponse
from testsystem.views.configuration_form import ConfigurationForm
from django.urls import reverse
from django.conf import settings
import os

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
    for file_name in os.listdir(file_path):
        if file_name.endswith('.yaml'):
            yaml = True
            yaml_file = file_name
        if file_name.endswith('.sh'):
            sh = True
            sh_file = file_name

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
    yaml_file_name = None

    for file_name in os.listdir(file_path):
        if file_name.endswith('.yaml'):
            yaml_file_name = file_name
            break

    if yaml_file_name:
        with open(os.path.join(file_path, yaml_file_name), 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/yaml')
            response['Content-Disposition'] = f'attachment; filename="{yaml_file_name}"'
            return response
    else:
        return HttpResponse("No se encontró ningún archivo .yaml en el directorio.")


def script_config_file(request):
    sh_file_name = None

    for file_name in os.listdir(file_path):
        if file_name.endswith('.sh'):
            sh_file_name = file_name
            break

    if sh_file_name:
        with open(os.path.join(file_path, sh_file_name), 'rb') as f:
            response = HttpResponse(
                f.read(), content_type='text/x-shellscript')
            response['Content-Disposition'] = f'attachment; filename="{sh_file_name}"'
            return response
    else:
        return HttpResponse("No se encontró ningún archivo .sh en el directorio.")
