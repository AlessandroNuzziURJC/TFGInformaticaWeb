import time
import threading

class Instance(threading.Thread):

    image = 'debian11'
    lock = threading.Lock()

    def __init__(self, execution, flavor, vcpus, queue) -> None:
        self.execution_unique_name = execution.execution_unique_name
        #self.keyname = 'Prueba2'
        self.flavor = flavor
        self.vcpus = int(vcpus)
        self.reps = execution.reps
        #self.results_path = resultsdir
        #self.log_path = logsdir
        self.instance_name = execution.execution_unique_name + '__' + self.flavor
        self.vol_name = execution.execution_unique_name + '__' + self.flavor + '__vol'
        self.execution = execution
        self.queue = queue
        self.thread = None

    def start_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run (self):
        for _ in range(1000000):
            pass
        print(self.instance_name)
        with self.lock:
            if self.execution.add_instance_run():
                self.queue.pop_executing_queue()