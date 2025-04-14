from ..model.task import Task

class TasksService:

    def __init__(self):
        self.tasks = []

    def __enter__(self):
        print("Utilizando biblioteca hello_world")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Fim do uso de biblioteca hello_world")

    def add_task(self, description: str):
        task = Task(description)
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks

    def remove_task(self, index: int):
        removed = None
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            return removed
        else:
            return removed