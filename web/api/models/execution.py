from datetime import datetime
import os
from django.conf import settings
from .instance import *

class Execution:

    instance_types_file_path = os.path.join(settings.BASE_DIR, 'api/files/instance_types.txt')

    def __init__(self, form_data, file) -> None:
        self.exec_name = form_data['exec_name']
        self.instance_types = form_data['instance_types']
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reps = form_data['reps']
        self.email = form_data['email']
        self.OpenMP = form_data['OpenMP']
        self.MPI = form_data['MPI']
        self.execution_unique_name = str(
            str(self.timestamp) + '__' + self.exec_name).replace(" ", "__")
        self.status = 'waiting'
        self.instances_run = 0
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
        self.instances_run = self.instances_run + 1
        return self.instances_run == self.max_instances_run

