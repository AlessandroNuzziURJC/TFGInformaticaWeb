import threading
from .models.execution_queue import *
from .models.openstack_service import *
from collections import deque

execution_queue = ExecutionQueue()
file_path = os.path.join(settings.BASE_DIR, 'api/files')
priority_queue = deque()


def daemon():
    if os.path.exists(file_path):
        while True:
            if exist_task():
                openstack = Openstack_Service()
                openstack.connect()
                execute_task(openstack)
                openstack.disconnect()

def execute_task(openstack):
    if len(priority_queue) > 0:
        next_instance = priority_queue[0]
        if openstack_instances_available(openstack, next_instance):
            instance = priority_queue.popleft()
            instance.start_thread()
    else:
        if not execution_queue.waiting_queue_is_empty():
            execution = execution_queue.next_execution()
            priority_queue.extend(execution.create_instances(execution_queue))

def exist_task():
    return len(priority_queue) != 0 or not execution_queue.waiting_queue_is_empty()

def openstack_instances_available(openstack, next_instance):
    limits = openstack.get_limits()
    instances_available =  int(limits['instances']) - int(limits['instances_used'])
    if instances_available == 0:
        return False
    cores_available = int(limits['maxTotalCores']) - int(limits['total_cores_used'])
    
    return #nextInstance cabe en cores avialable


thread_imprimir = threading.Thread(target=daemon)
thread_imprimir.daemon = True  # Esto permite que el subproceso se detenga cuando se detiene el programa principal
thread_imprimir.start()