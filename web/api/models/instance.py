import threading
import subprocess

from .email_sender import *

class Instance(threading.Thread):
    """
    Clase para manejar la creación y ejecución de instancias en hilos separados.

    Attributes:
        image (str): Imagen de la instancia.
        lock (threading.Lock): Candado para evitar condiciones de carrera.
        create_instance_script (str): Ruta al script de creación de instancia.
        execute_program_script (str): Ruta al script de ejecución de programa.
        delete_instance_script (str): Ruta al script de eliminación de instancia.
    """

    image = 'debian11'
    lock = threading.Lock()
    create_instance_script = './api/scripts/createInstance.sh'
    execute_program_script = './api/scripts/executeProgram.sh'
    delete_instance_script = './api/scripts/deleteInstance.sh'

    def __init__(self, execution, flavor, vcpus, queue) -> None:
        """
        Inicializa la instancia de la clase Instance.

        Args:
            execution (Execution): Objeto Execution que contiene los datos de la ejecución.
            flavor (str): Tipo de instancia.
            vcpus (int): Número de CPUs de la instancia.
            queue (Queue): Objeto Queue para gestionar las ejecuciones en la cola.
        """
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
        """
        Inicia un hilo para la ejecución de la instancia.
        """
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run (self):
        """
        Ejecuta la creación y ejecución de la instancia en un hilo separado.

        Cuando la ejecución se completa, si se añade correctamente a la instancia,
        se elimina de la cola de ejecución y se envía un correo electrónico.
        """
        self.create_instance()
        with self.lock:
            if self.execution.add_instance_run():
                self.queue.pop_executing_queue(self.execution)
                email = EmailSender(self.execution.exec_name, self.execution.email)
                email.send()

    def create_instance(self):
        """
        Llama al script de creación de instancia, ejecuta el programa y elimina la instancia.

        Args:
            No recibe argumentos.

        Returns:
            No devuelve nada.
        """
        aux_output = './output/' + self.execution_unique_name +'/results/c_' + self.flavor[1:] + '_.txt'
        installation_time = './output/' + self.execution_unique_name + '/installation_time/' + self.flavor + '.txt'
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

    