import threading
import subprocess

from .email_sender import *

class Instance(threading.Thread):

    image = 'debian11'
    lock = threading.Lock()
    create_instance_script = './api/scripts/createInstance.sh'
    execute_program_script = './api/scripts/executeProgram.sh'
    delete_instance_script = './api/scripts/deleteInstance.sh'

    def __init__(self, execution, flavor, vcpus, queue) -> None:
        self.execution_unique_name = execution.execution_unique_name
        self.keyname = 'key_testsystem'
        self.flavor = flavor
        self.vcpus = int(vcpus)
        self.reps = execution.reps
        self.log_path = './output/' + self.execution_unique_name + '/logs'
        self.results_path = './output/' + self.execution_unique_name + '/results'

        self.instance_name = execution.execution_unique_name + '__' + self.flavor
        self.vol_name = execution.execution_unique_name + '__' + self.flavor + '__vol'
        self.execution = execution
        self.queue = queue
        self.thread = None

    def start_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run (self):
        self.create_instance()
        with self.lock:
            if self.execution.add_instance_run():
                self.queue.pop_executing_queue(self.execution)
                email = EmailSender(self.execution.exec_name, self.execution.email)
                email.send()

    def create_instance(self):
        """
        Ejecuta el script de creacion de instancia.

        Args:

        Returns:

        """
        aux_output = './output/' + self.execution_unique_name +'/results/c_' + self.flavor[1:] + '_.txt'
        installation_time = './output/' + self.execution_unique_name + '/installation_time.txt'
        threads = 0
        if self.execution.MPI or self.execution.OpenMP:
            threads = self.vcpus
        with open(self.log_path + '/execution_' + self.flavor + '_.txt', 'a') as outfile:
            subprocess.call([self.create_instance_script, self.flavor, self.image,
                            self.keyname, self.instance_name, self.vol_name, 
                            self.execution_unique_name, str(self.execution.MPI), 
                            str(self.execution.OpenMP), installation_time], stdout=outfile, stderr=outfile)
            for i in range(0, int(self.reps)):
                #Change seed
                subprocess.call([self.execute_program_script, self.flavor, self.image,
                            self.keyname, self.instance_name, self.vol_name, 
                            self.execution_unique_name, aux_output, 
                            str(self.execution.MPI), str(self.execution.OpenMP), str(threads)], 
                            stdout=outfile, stderr=outfile)
            subprocess.call([self.delete_instance_script, self.flavor, self.image,
                            self.keyname, self.instance_name, self.vol_name, self.execution_unique_name], stdout=outfile, stderr=outfile)

    