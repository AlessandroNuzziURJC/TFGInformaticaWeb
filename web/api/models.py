from collections import deque
from datetime import datetime
import os
from django.conf import settings

class ExecutionQueue:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.queue = deque()
        return cls._instance

    def append(self, execution):
        self.queue.append(execution)

    def pop(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return None
    

class Execution:

    def __init__(self, form_data, file) -> None:
        self.exec_name = form_data['exec_name']
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reps = form_data['reps']
        self.email = form_data['email']
        self.OpenMP = form_data['OpenMP']
        self.MPI = form_data['MPI']
        self.instance_name = str(
            str(self.timestamp) + self.exec_name).replace(" ", "_")
        self.status = 'waiting'
        self.createdirs()
        self.save(file)

    def to_dict(self):
        output = vars(self)
        return output
    
    def createdirs(self):
        """
        Crea los directorios necesarios para la ejecucion.

        Args:

        Returns:

        """
        if not os.path.exists('./output'):
            os.makedirs('./output')

        if not os.path.exists('./output/' + self.instance_name):
            os.makedirs('./output/' + self.instance_name)

        if not os.path.exists('./output/' + self.instance_name + '/logs'):
            os.makedirs('./output/' + self.instance_name + '/logs')

        if not os.path.exists('./output/' + self.instance_name + '/results'):
            os.makedirs('./output/' + self.instance_name + '/results')

        if not os.path.exists('./output/' + self.instance_name + '/time'):
            os.makedirs('./output/' + self.instance_name + '/time')

        if not os.path.exists('./output/' + self.instance_name + '/program'):
            os.makedirs('./output/' + self.instance_name + '/program')
    
    def save(self, program_file):
        with open('./output/' + self.instance_name + '/informacion.txt', 'w') as file:
            file.write(f"Nombre de la ejecucion: {self.exec_name}\n")
            file.write(f"Fecha y hora de la ejecucion: {self.timestamp}\n")
            file.write(f"Numero de pruebas: {self.reps}\n")
            file.write(f"Email donde notificar: {self.email}\n")
            file.write(f"OpenMP: {self.OpenMP}\n")
            file.write(f"MPI: {self.MPI}\n")
            file.write(f"Nombre de la instancia: {self.instance_name}\n")

        ubicacion = os.path.join(
            settings.MEDIA_ROOT, './output/' + self.instance_name + '/program', program_file.name)
        with open(ubicacion, 'wb') as destino:
            for chunk in program_file.chunks():
                destino.write(chunk)