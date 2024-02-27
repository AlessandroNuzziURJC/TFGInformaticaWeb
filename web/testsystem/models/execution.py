from datetime import datetime

class Execution:

    def __init__(self, form_data=None, file=None, execution_unique_name=None) -> None:
        if execution_unique_name == None:
            self.exec_name = form_data['exec_name']
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
            Lee los datos de la ejecucion desde los archivos.

        Args:
            execution_unique_name: identificador de la ejecucion
        Returns:

        """
        with open('./output/' + execution_unique_name + '/informacion.txt', 'r') as f:
            self.exec_name = f.readline().split(':')[1]
            self.timestamp = datetime.strptime(f.readline().split(': ')[1].strip(), "%Y-%m-%d %H:%M:%S")
            self.reps = int(f.readline().split(':')[1].strip())
            self.email = f.readline().split(':')[1].strip()
            self.OpenMP = f.readline().split(':')[1].strip().__contains__('True')
            self.MPI = f.readline().split(':')[1].strip().__contains__('True')
            self.execution_unique_name = execution_unique_name


    def get_execution_info(self):
        output = {}
        output['exec_name'] = self.exec_name
        output['reps'] = self.reps
        output['email'] = self.email
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