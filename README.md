## Simple DAG Framework to run a set of tasks in a ordered fashion

```
In [1]: from dags.task_runner import TaskRunner

In [2]: from dags import dag_example

In [3]: TaskRunner(module=dag_example).run_tasks()
```

```
Running Task Task0 which depends on []
Running Task Task1 which depends on [Task0]
Running Task Task2 which depends on [Task0]
Running Task Task4 which depends on [Task1]
Running Task Task3 which depends on [Task1, Task2, Task4]
5 task(s) ran successfully
```
