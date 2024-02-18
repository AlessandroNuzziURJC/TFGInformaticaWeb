from datetime import datetime

class Execution:

    def __init__(self, form_data, file) -> None:
        self.exec_name = form_data['exec_name']
        #self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reps = form_data['reps']
        self.email = form_data['email']
        #self.file = file
        file_content = ""
        for chunk in file.chunks():
            file_content += chunk.decode('utf-8')

        self.OpenMP = file_content.__contains__('#include <omp.h>')
        self.MPI = file_content.__contains__('#include <mpi.h>')