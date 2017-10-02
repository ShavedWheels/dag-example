from task_runner import BaseTask


class Task0(BaseTask):

    def run_task(self):
        pass


class Task1(BaseTask):

    dependencies = [Task0]

    def run_task(self):
        pass


class Task2(BaseTask):

    dependencies = [Task0]

    def run_task(self):
        pass


class Task4(BaseTask):

    dependencies = [Task1]

    def run_task(self):
        pass


class Task3(BaseTask):

    dependencies = [Task1, Task2, Task4]

    def run_task(self):
        pass


