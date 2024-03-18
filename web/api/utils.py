import threading
from .models.execution_queue import *
from .models.openstack_service import *
from collections import deque
import time

execution_queue = ExecutionQueue()
file_path = os.path.join(settings.BASE_DIR, 'api/files')
priority_queue = deque()


def daemon():
    """
    Función de daemon que gestiona la ejecución de tareas en segundo plano.

    Esta función verifica periódicamente si existen tareas en la cola de prioridad o en la cola de espera de ejecución.
    Si hay tareas pendientes y los recursos de OpenStack están disponibles, inicia su ejecución.

    Args:

    Returns:
    """
    if os.path.exists(file_path):
        while True:
            time.sleep(60)
            print('Starting daemon check', time.ctime(time.time()))
            if exist_task():
                print('Found tasks', time.ctime(time.time()))
                openstack = OpenstackService()
                openstack.connect()
                execute_task(openstack)
                openstack.disconnect()
                

def execute_task(openstack):
    """
    Ejecuta la próxima tarea en la cola de prioridad o asigna recursos a las tareas en espera.

    Args:
        openstack: Servicio de OpenStack para la gestión de recursos.

    Returns:
    """
    limits = openstack.get_limits()

    free_vcpus = int(limits['maxTotalCores']) - int(limits['total_cores_used'])
    free_instances = int(limits['instances']) - int(limits['instances_used'])


    while free_vcpus > 0 and free_instances > 0:

        if len(priority_queue) == 0:
            if (not execution_queue.waiting_queue_is_empty()):
                execution = execution_queue.next_execution()
                priority_queue.extend(execution.create_instances(execution_queue))
            else:
                return

        next_instance = priority_queue[0]
        if openstack_instances_available(openstack, next_instance):
            free_vcpus = free_vcpus - next_instance.vcpus
            free_instances = free_instances - 1
            instance = priority_queue.popleft()
            instance.start_thread()
        else:
            return


def exist_task():
    """
    Verifica si existen tareas pendientes en la cola de prioridad o en la cola de espera de ejecución.

    Returns:
        True si hay tareas pendientes, False de lo contrario.
    """
    return len(priority_queue) != 0 or not execution_queue.waiting_queue_is_empty()

def openstack_instances_available(openstack, next_instance):
    """
    Verifica si hay suficientes recursos disponibles en OpenStack para la próxima instancia.

    Args:
        openstack: Servicio de OpenStack para la gestión de recursos.
        next_instance: Próxima instancia a ejecutar.

    Returns:
        True si hay suficientes recursos disponibles, False de lo contrario.
    """
    limits = openstack.get_limits()
    instances_available =  int(limits['instances']) - int(limits['instances_used'])
    if instances_available == 0:
        return False
    cores_available = int(limits['maxTotalCores']) - int(limits['total_cores_used'])
    return next_instance.vcpus <= cores_available


thread_empty_executions = threading.Thread(target=daemon)
thread_empty_executions.daemon = True 
thread_empty_executions.start()