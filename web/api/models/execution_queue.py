from collections import deque


class ExecutionQueue:
    """
    Representa una cola de ejecuciones.

    Atributos:
        _instance (ExecutionQueue): Instancia única de la cola.
        waiting_queue (deque): Cola de ejecuciones en espera.
        executing_queue (deque): Cola de ejecuciones en ejecución.
    """

    _instance = None

    def __new__(cls):
        """
        Crea una nueva instancia única de ExecutionQueue si no existe.

        Returns:
            ExecutionQueue: Instancia única de la cola.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.waiting_queue = deque()
            cls._instance.executing_queue = deque()
        return cls._instance

    def append_waiting_queue(self, execution):
        """
        Agrega una ejecución a la cola de espera.

        Args:
            execution (Execution): Ejecución a agregar.
        """
        self.waiting_queue.append(execution)     

    def next_execution(self):
        """
        Obtiene la próxima ejecución en la cola de espera y la mueve a la cola de ejecución.

        Returns:
            Execution: Ejecución obtenida.
        """
        if len(self.waiting_queue) > 0:
            execution = self.waiting_queue.popleft()
            execution.status = 'running'
            self.executing_queue.append(execution)
            return execution
        return None
    
    def pop_executing_queue(self, execution):
        """
        Elimina una ejecución de la cola de ejecución.

        Args:
            execution (Execution): Ejecución a eliminar de la cola de ejecución.
        Returns:
            bool: True si se eliminó la ejecución, False si no se encontró.
        """
        if len(self.executing_queue) > 0:
            return self.executing_queue.remove(execution)
        return None
    
    def is_empty(self):
        """
        Comprueba si la cola está vacía.

        Returns:
            bool: True si la cola está vacía, False si tiene elementos.
        """
        return len(self.waiting_queue) + len(self.executing_queue) == 0
    
    def waiting_queue_is_empty(self):
        """
        Comprueba si la cola de espera está vacía.

        Returns:
            bool: True si la cola de espera está vacía, False si tiene elementos.
        """
        return len(self.waiting_queue) == 0
