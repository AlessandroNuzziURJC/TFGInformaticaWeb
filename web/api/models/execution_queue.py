from collections import deque


class ExecutionQueue:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.waiting_queue = deque()
            cls._instance.executing_queue = deque()
        return cls._instance

    def append_waiting_queue(self, execution):
        self.waiting_queue.append(execution)     

    def next_execution(self):
        if len(self.waiting_queue) > 0:
            execution = self.waiting_queue.popleft()
            execution.status = 'running'
            self.executing_queue.append(execution)
            return execution
        return None
    
    def pop_executing_queue(self, execution):
        if len(self.executing_queue) > 0:
            return self.executing_queue.remove(execution)
        return None
    
    def is_empty(self):
        return len(self.waiting_queue) + len(self.executing_queue) == 0
    
    def waiting_queue_is_empty(self):
        return len(self.waiting_queue) == 0
