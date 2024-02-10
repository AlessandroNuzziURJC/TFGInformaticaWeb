from collections import deque
from datetime import datetime

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
        self.instance_name = form_data['instance_name']
        #self.file = file
        self.status = 'waiting'

    def to_dict(self):
        return vars(self)