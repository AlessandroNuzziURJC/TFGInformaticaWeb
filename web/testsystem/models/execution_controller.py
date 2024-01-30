from collections import deque


class ExecutionController:

    def __init__(self) -> None:
        self.queue = deque()

    def add(self, execution):
        self.queue.append(execution)