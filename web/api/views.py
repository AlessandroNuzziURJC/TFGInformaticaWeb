import os
from .utils import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models.execution_queue import *
from .models.execution import *
import json


execution_queue = ExecutionQueue()
file_path = os.path.join(settings.BASE_DIR, 'api/files')


@csrf_exempt
def enqueue(request):
    if request.method == 'POST':
        try:
            aux = dict()
            aux['exec_name'] = request.POST.get('exec_name')
            aux['reps'] = int(request.POST.get('reps'))
            aux['email'] = request.POST.get('email')
            aux['OpenMP'] = bool(request.POST.get('OpenMP'))
            aux['MPI'] = bool(request.POST.get('MPI'))

            program_file = request.FILES.get('program')
            execution = Execution(aux, program_file)
            execution_queue.append_waiting_queue(execution)
            return JsonResponse({"message": "Object enqueued successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_queue(request):
    if request.method == 'GET':
        waiting_queue_content = [execution.to_dict()
                         for execution in execution_queue.waiting_queue]
        executing_queue_content = [execution.to_dict()
                         for execution in execution_queue.executing_queue]
        return JsonResponse({"queue": executing_queue_content + waiting_queue_content})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def store_conf_files(request):
    if request.method == 'POST':
        try:
            file_sh = request.FILES['file_sh']
            file_yaml = request.FILES['file_yaml']

            if not os.path.exists(file_path):
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

            openstack = Openstack_Service()
            openstack.connect()
            path = os.path.join(
                settings.BASE_DIR, file_path, 'instance_types.txt')
            with open(path, 'w') as file:
                instances = openstack.instances_available()
                for e in instances:
                    file.write(e + '\n')
            openstack.disconnect()

            return JsonResponse({"message": "Configuration files received."})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error in configuration files transfer."}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_yaml_conf_file(request):
    yaml_file_name = None

    if not os.path.exists(file_path):
        os.makedirs(file_path)

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


def get_sh_conf_file(request):
    sh_file_name = None

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for file_name in os.listdir(file_path):
        if file_name.endswith('.sh'):
            sh_file_name = file_name
            break

    if sh_file_name:
        with open(os.path.join(file_path, sh_file_name), 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/sh')
            response['Content-Disposition'] = f'attachment; filename="{sh_file_name}"'
            return response
    else:
        return HttpResponse("No se encontró ningún archivo .sh en el directorio.")


def exists_conf_files(request):
    output = {'yaml_file_name': None, 'sh_file_name': None}

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for file_name in os.listdir(file_path):
        if file_name.endswith('.yaml'):
            output['yaml_file_name'] = file_name
        if file_name.endswith('.sh'):
            output['sh_file_name'] = file_name

    return JsonResponse(output)

