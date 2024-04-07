from datetime import datetime
import os
from django.conf import settings
from .instance import *

import threading

class UniqueIdentifier:
    _counter = max(int(elem.split('_')[0]) for elem in os.listdir('./output') if os.path.isdir(os.path.join('./output', elem)))
    _lock = threading.Lock()

    @classmethod
    def generate(cls):
        with cls._lock:
            cls._counter += 1
            return cls._counter


class Execution:
    """
    Representa una ejecución de programa con sus detalles.

    Atributos:
        instance_types_file_path (str): Ruta al archivo de tipos de instancia.
        exec_name (str): Nombre de la ejecución.
        instance_types (list): Lista de tipos de instancia.
        timestamp (str): Marca de tiempo de la ejecución.
        reps (int): Número de repeticiones de la ejecución.
        email (str): Correo electrónico para notificaciones.
        OpenMP (bool): Indicador de uso de OpenMP.
        MPI (bool): Indicador de uso de MPI.
        execution_unique_name (str): Nombre único de la ejecución.
        status (str): Estado de la ejecución.
        instances_run (int): Número de instancias en ejecución.
        max_instances_run (int): Número máximo de instancias en ejecución.
    """

    instance_types_file_path = os.path.join(settings.BASE_DIR, 'api/files/instance_types.txt')

    def __init__(self, form_data, file) -> None:
        """
        Inicializa una instancia de Execution.

        Args:
            form_data (dict): Datos del formulario.
            file (File): Archivo de programa.
        """
        self.exec_name = form_data['exec_name']
        self.instance_types = form_data['instance_types']
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        self.reps = form_data['reps']
        self.email = form_data['email']
        self.OpenMP = form_data['OpenMP']
        self.MPI = form_data['MPI']
        self.execution_unique_name = str(str(UniqueIdentifier.generate()) + '__' +
            str(self.timestamp) + '__' + self.exec_name).replace(" ", "__")
        self.status = 'waiting'
        self.instances_run = 0
        self.createdirs()
        self.save(file)

    def to_dict(self):
        """
        Convierte los atributos de la ejecución en un diccionario.

        Returns:
            dict: Atributos de la ejecución.
        """
        output = vars(self)
        return output

    def createdirs(self):
        """
        Crea los directorios necesarios para la ejecución.
        """
        if not os.path.exists('./output'):
            os.makedirs('./output')

        if not os.path.exists('./output/' + self.execution_unique_name):
            os.makedirs('./output/' + self.execution_unique_name)

        if not os.path.exists('./output/' + self.execution_unique_name + '/logs'):
            os.makedirs('./output/' + self.execution_unique_name + '/logs')

        if not os.path.exists('./output/' + self.execution_unique_name + '/results'):
            os.makedirs('./output/' + self.execution_unique_name + '/results')

        if not os.path.exists('./output/' + self.execution_unique_name + '/program'):
            os.makedirs('./output/' + self.execution_unique_name + '/program')

        if not os.path.exists('./output/' + self.execution_unique_name + '/installation_time'):
            os.makedirs('./output/' + self.execution_unique_name + '/installation_time')

    def save(self, program_file):
        """
        Guarda los detalles de la ejecución y el programa.

        Args:
            program_file (File): Archivo de programa.
        """
        with open('./output/' + self.execution_unique_name + '/informacion.txt', 'w') as file:
            file.write(f"Nombre de la ejecucion: {self.exec_name}\n")
            file.write(f"Instancias: {self.instance_types}\n")
            file.write(f"Fecha y hora de la ejecucion: {self.timestamp}\n")
            file.write(f"Numero de pruebas: {self.reps}\n")
            file.write(f"Email donde notificar: {self.email}\n")
            file.write(f"OpenMP: {self.OpenMP}\n")
            file.write(f"MPI: {self.MPI}\n")
            file.write(f"Nombre único de la ejecución: {self.execution_unique_name}\n")

        ubicacion = os.path.join(
            settings.MEDIA_ROOT, './output/' + self.execution_unique_name + '/program', program_file.name)
        with open(ubicacion, 'wb') as destino:
            for chunk in program_file.chunks():
                destino.write(chunk)

    def create_instances(self, queue):
        """
        Crea instancias de ejecución.

        Args:
            queue (ExecutionQueue): Cola de ejecuciones.

        Returns:
            list: Lista de instancias creadas.
        """
        output = []
        instance_types = []
        with open(self.instance_types_file_path, 'r') as file:
            for line in file:
                instance_types.append(line.split(' ')[0])

        for elem in self.instance_types:
            if elem not in instance_types:
                raise Exception("Instances not valid.")

        self.max_instances_run = len(self.instance_types)

        for flavor in self.instance_types:
            output.append(Instance(self, flavor, flavor[1:], queue))
        return output
    
    def add_instance_run(self):
        """
        Añade una instancia ejecutada.

        Returns:
            bool: True si se ha alcanzado el límite de instancias ejecutadas, False en caso contrario.
        """
        self.instances_run = self.instances_run + 1
        return self.instances_run == self.max_instances_run

