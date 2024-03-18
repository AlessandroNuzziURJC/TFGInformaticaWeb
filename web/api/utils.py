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
            if exist_task():
                time.sleep(60)
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
    if len(priority_queue) > 0:
        next_instance = priority_queue[0]
        if openstack_instances_available(openstack, next_instance):
            instance = priority_queue.popleft()
            instance.start_thread()
    else:
        if (not execution_queue.waiting_queue_is_empty()) and availability(openstack):
            execution = execution_queue.next_execution()
            priority_queue.extend(execution.create_instances(execution_queue))


def exist_task():
    """
    Verifica si existen tareas pendientes en la cola de prioridad o en la cola de espera de ejecución.

    Returns:
        True si hay tareas pendientes, False de lo contrario.
    """
    return len(priority_queue) != 0 or not execution_queue.waiting_queue_is_empty()

def availability(openstack):
    """
    Verifica la disponibilidad de recursos en OpenStack.

    Args:
        openstack: Servicio de OpenStack para la gestión de recursos.

    Returns:
        True si hay recursos disponibles, False de lo contrario.
    """
    limits = openstack.get_limits()
    return int(limits['maxTotalCores']) - int(limits['total_cores_used']) > 0 and int(limits['instances']) - int(limits['instances_used']) > 0

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