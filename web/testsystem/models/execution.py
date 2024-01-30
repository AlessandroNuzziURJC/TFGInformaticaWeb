from datetime import datetime

class Execution:

    def __init__(self, form_data, file) -> None:
        self.exec_name = form_data['name']
        self.timestamp = datetime.now()
        self.instance_flavor = form_data['instance_type']
        self.reps = form_data['reps']
        self.email = form_data['email']
        self.OpenMP = form_data['lib'].__contains__("OpenMP")
        self.MPI = form_data['lib'].__contains__("MPI")
        self.instance_name = str(
            str(self.timestamp) + self.exec_name).replace(" ", "_")
        self.file = file
        self.status = 'waiting'