import os
import shutil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models import *  
import json

execution_queue = ExecutionQueue()
file_path = os.path.join(settings.BASE_DIR, 'api/files')

@csrf_exempt
def enqueue(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            execution_queue.append(Execution(data, None))
            return JsonResponse({"message": "Object enqueued successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in request body"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
def get_queue(request):
    if request.method == 'GET':
        queue_content = [execution.to_dict() for execution in execution_queue.queue]
        return JsonResponse({"queue": queue_content})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def store_conf_files(request):
    if request.method == 'POST':
        try:
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

            return JsonResponse({"message": "Configuration files received."})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error in configuration files transfer."}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
def get_yaml_conf_file(request):
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
    
def get_sh_conf_file(request):
    sh_file_name = None

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
    
def exists_yaml_conf_file(request):
    for file_name in os.listdir(file_path):
        if file_name.endswith('.yaml'):
            return JsonResponse({'name': file_name})
        
    return JsonResponse({'name': None})

def exists_sh_conf_file(request):
    for file_name in os.listdir(file_path):
        if file_name.endswith('.sh'):
            return JsonResponse({'name': file_name})
        
    return JsonResponse({'name': None})