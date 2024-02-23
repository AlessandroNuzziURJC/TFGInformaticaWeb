import threading
import subprocess

class Instance(threading.Thread):

    image = 'debian11'
    lock = threading.Lock()
    create_instance_script = './api/scripts/createInstance.sh'
    execute_program_script = './api/scripts/executeProgram.sh'
    delete_instance_script = './api/scripts/deleteInstance.sh'

    def __init__(self, execution, flavor, vcpus, queue) -> None:
        self.execution_unique_name = execution.execution_unique_name
        self.keyname = 'Prueba2'
        self.flavor = flavor
        self.vcpus = int(vcpus)
        self.reps = execution.reps
        #self.results_path = resultsdir
        #self.log_path = logsdir
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
                self.queue.pop_executing_queue()

    def create_instance(self):
        """
        Ejecuta el script de creacion de instancia.

        Args:

        Returns:

        """
        with open(self.log_path + '/execution_' + self.flavor + '_.txt', 'a') as outfile:
            subprocess.call([self.create_instance_script, self.flavor, self.image,
                            self.keyname, self.instance_name, self.vol_name, self.execution_unique_name], stdout=outfile, stderr=outfile)
            for i in range(0, int(self.reps)):
                subprocess.call([self.execute_program_script, self.flavor, self.image,
                            self.keyname, self.instance_name, self.vol_name, self.execution_unique_name], stdout=outfile, stderr=outfile)
            subprocess.call([self.delete_instance_script, self.flavor, self.image,
                            self.keyname, self.instance_name, self.vol_name, self.execution_unique_name], stdout=outfile, stderr=outfile)

    