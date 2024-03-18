from datetime import datetime


class Execution:
    """
    Clase para manejar la información de una ejecución.

    Esta clase permite crear una instancia de una ejecución,
    ya sea a partir de datos proporcionados mediante un formulario o desde archivos.

    Attributes:
        exec_name (str): Nombre de la ejecución.
        instance_types (list): Tipos de instancia utilizados en la ejecución.
        reps (int): Número de repeticiones de la ejecución.
        email (str): Correo electrónico asociado a la ejecución.
        OpenMP (bool): Indica si se utilizó OpenMP en la ejecución.
        MPI (bool): Indica si se utilizó MPI en la ejecución.
        execution_unique_name (str): Identificador único de la ejecución.
        timestamp (datetime): Marca de tiempo de la ejecución.
    """

    def __init__(self, form_data=None, file=None, execution_unique_name=None) -> None:
        """
        Inicializa la instancia de la ejecución.

        Si se proporcionan form_data y file, se crea una nueva ejecución.
        Si se proporciona execution_unique_name, se lee la información desde archivos.

        Args:
            form_data (dict): Datos del formulario.
            file (file): Archivo enviado.
            execution_unique_name (str): Identificador único de la ejecución.
        """
        if execution_unique_name == None:
            self.exec_name = form_data['exec_name']
            self.instance_types = form_data['instance_types']
            self.reps = form_data['reps']
            self.email = form_data['email']
            file_content = ""
            for chunk in file.chunks():
                file_content += chunk.decode('utf-8')

            self.OpenMP = file_content.__contains__('#include <omp.h>')
            self.MPI = file_content.__contains__('#include <mpi.h>')
        else:
            self.read_from_file(execution_unique_name)

    def read_from_file(self, execution_unique_name):
        """
        Lee los datos de la ejecución desde los archivos.

        Args:
            execution_unique_name (str): Identificador único de la ejecución.
        """
        with open('./output/' + execution_unique_name + '/informacion.txt', 'r') as f:
            self.exec_name = f.readline().split(':')[1]
            self.instance_types = eval(f.readline().split(':')[1])
            self.timestamp = datetime.strptime(
                f.readline().split(': ')[1].strip(), "%Y-%m-%d %H:%M:%S")
            self.reps = int(f.readline().split(':')[1].strip())
            self.email = f.readline().split(':')[1].strip()
            self.OpenMP = f.readline().split(
                ':')[1].strip().__contains__('True')
            self.MPI = f.readline().split(':')[1].strip().__contains__('True')
            self.execution_unique_name = execution_unique_name

    def get_execution_info(self):
        """
        Obtiene la información de la ejecución en un formato adecuado para mostrar.

        Returns:
            dict: Diccionario con la información de la ejecución.
        """
        output = {}
        output['exec_name'] = self.exec_name
        output['reps'] = self.reps
        output['email'] = self.email
        aux_instance_list = []
        for i in self.instance_types:
            aux_instance_list.append(i + ' ')
        output['instance_types'] = aux_instance_list
        aux = 'Ninguna'
        if self.OpenMP and self.MPI:
            aux = 'OpenMP y OpenMPI'
        elif self.OpenMP:
            aux = 'OpenMP'
        elif self.MPI:
            aux = 'MPI'

        output['libs'] = aux
        timestamp_div = str(self.timestamp).split()
        output['date'] = timestamp_div[0]
        output['hour'] = timestamp_div[1]
        output['execution_unique_name'] = self.execution_unique_name
        return output
