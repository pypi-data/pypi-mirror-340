from hello_world import TasksService

def main():
    with TasksService() as service:
        service.add_task("Estudar context manager")
        service.add_task("Finalizar projeto")
        tasks = service.list_tasks()

        for idx, task in enumerate(tasks):
            print(f"{idx}: {task.description}")

if __name__ == "__main__":
    main()