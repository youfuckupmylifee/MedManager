class Task():
    def __init__(self, task_name, description, deadline, status):
        self.task_name = task_name
        self.description = description
        self.deadline = deadline
        self.status = status
        self.observer = []
        self.state = UncompletedStatus(self)

    def change_status(self):
        self.state.change_status()

    def print_information(self):
        print(self.task_name)
        print(self.description)
        print(self.deadline)
        print(self.status)

    def add_observer(self, observer):
        self.state.add_observer(observer)

    def remove_observer(self, observer):
        self.state.remove_observer(observer)

    def notify_observer(self):
        self.state.notify_observer()

class Project():
    def __init__(self, project_name, description):
        self.project_name = project_name
        self.description = description
        self.task_list = []

    def add_task(self, task_name, description, deadline, status):
        task = Task(task_name, description, deadline, status)
        self.task_list.append(task)

    def del_task(self, task_name):
        self.task_list = [task for task in self.task_list if task.task_name != task_name]

    def print_task(self):
        for task in self.task_list:
            task.print_information()
            print("--------")

# Паттерн 'Фабричный метод'
class TaskCreator:
    def create_task(self, task_name, description, deadline, status):
        pass

class ConcreteTaskCreator1(TaskCreator):
    def create_task(self, task_name, description, deadline, status):
        return Task(task_name, description, deadline, status)

class ConcreteTaskCreator2(TaskCreator):
    def create_task(self, task_name, description, deadline, status):
        return Task(task_name, description, deadline, status)

# Паттерн 'Наблюдатель'
class TaskObserver:
    def update(self, task):
        # Этот метод вызывается, когда у задачи наступает срок выполнения
        print(f"Задача '{task.task_name}' должна быть выполнена до {task.deadline}!")

# Паттерн 'Состояния'
class StatusState:
    def __init__(self, task):
        self.task = task

    def change_status(self):
        pass

    def add_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass

class CompletedStatus(StatusState):
    def change_status(self):
        print('Задача невыполнена')
        self.task.status = 'Uncompleted'
        self.task.state = UncompletedStatus(self.task)

class UncompletedStatus(StatusState):
    def change_status(self):
        print('Задача выполнена')
        self.task.status = 'Completed'
        self.task.state = CompletedStatus(self.task)

class Status:
    def __init__(self):
        self.state = UncompletedStatus()

    def completed(self):
        self.state = self.state.completed()

    def uncompleted(self):
        self.state = self.state.uncompleted()

# Создаем экземпляр класса Project
project = Project("Task_and_project_management", "Какое-то описание проекта")

# Пример использования паттерна 'Фабричный метод'
creator = ConcreteTaskCreator1()
task1 = creator.create_task("Task 1", "Какое-то описание для задачи", "2023-12-31", False)
project.add_task(task1.task_name, task1.description, task1.deadline, task1.status)

creator = ConcreteTaskCreator2()
task2 = creator.create_task("Task 2", "Какое-то описание для задачи", "2023-12-15", False)
project.add_task(task2.task_name, task2.description, task2.deadline, task2.status)

creator = ConcreteTaskCreator1()
task3 = creator.create_task("Task 3", "Какое-то описание для задачи", "2025-12-10", False)
project.add_task(task3.task_name, task3.description, task3.deadline, task3.status)

# Выводим задачи проекта
print("Проект:", project.project_name)
print("Описание:", project.description)
print("Задачи:")
project.print_task()

# Пример использования паттерна 'Наблюдатель'
observer = TaskObserver()
task1.add_observer(observer)

# Когда срок выполнения наступает, уведомляем наблюдателей
task1.notify_observer()

# Используем паттерн 'Состояние'
task1.change_status()
project.print_task()