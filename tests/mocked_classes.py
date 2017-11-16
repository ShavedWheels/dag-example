from dags.task_runner import BaseTask


class A(BaseTask):

    def run_task(self):
        pass


class B(BaseTask):
    dependencies = [A]

    def run_task(self):
        pass


class D(BaseTask):
    def run_task(self):
        pass


class C(BaseTask):
    dependencies = [A, B, D]

    def run_task(self):
        pass


class E(BaseTask):

    dependencies = []

    def run_task(self):
        pass


class F(BaseTask):

    def run_task(self):
        pass


class G(BaseTask):

    dependencies = [F]

    def run_task(self):
        pass
