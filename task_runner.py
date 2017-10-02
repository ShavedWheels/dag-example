import inspect
from abc import ABCMeta, abstractmethod


DEPENDENCIES = 'dependencies'


class BaseTask(object):

    __metaclass__ = ABCMeta

    dependencies = []

    is_base_task = True

    @abstractmethod
    def run_task(self):
        """This method acts a placement holder. All inherited classes (tasks) MUST override this run_task method"""
        pass

    def run(self):
        dependencies = ", ".join(task.__name__ for task in self.dependencies)
        task_name = self.__class__.__name__
        print "Running Task {task_name} which depends on [{dependencies}]".format(
            task_name=task_name, dependencies=dependencies
        )
        self.run_task()


class TaskRunner(object):
    """
    Uses a directed acyclic graph to run a set of tasks
    """
    def __init__(self, module):
        """
        :param module: module containing our tasks
        """
        self.module = module

    def get_tasks(self):
        """
        Given a module, gets all objects which satisfy following criteria:
        1. Is a class
        2. Has a class attribute of 'dependencies
        3. Is not a base class (i.e. only inherits from object)
        :return: list containing relevant classes
        """
        task_list = []
        for name, obj in inspect.getmembers(self.module, predicate=inspect.isclass):
            try:
                assert obj.__base__.is_base_task
                if hasattr(obj, DEPENDENCIES):
                    task_list.append(obj)
            except AttributeError as e:
                if name == BaseTask.__name__:
                    continue
                else:
                    raise Exception("{cls} Error: {error}".format(error=e,cls=name))

        assert len(task_list) > 0
        return task_list

    @staticmethod
    def task_has_dependencies(obj):
        """
        Checks to see whether the object in question has a class attribute of 'dependencies'. If it does, check that
        there are more than one members in the list.
        :param obj: object to check
        :return: boolean
        """
        try:
            dependencies = getattr(obj, DEPENDENCIES)
            if len(dependencies) > 0:
                return True
        except AttributeError:
            return False

    def get_task_order(self, task):
        """
        Calculate the run order given a task and, where applicable, its dependencies
        Step 1: check whether the task has any dependencies, if it doesn't, add it to our list
        Step 2: get all the dependent tasks and recursively check if they have dependencies. Once a task has been found
        with no dependencies we add it to our list
        :param task: task
        :return: list containing tasks in a ordered fashion (may contain duplicates)
        """
        task_list = []
        if self.task_has_dependencies(task):
            depends_on_list = getattr(task, DEPENDENCIES)
            for dependency in depends_on_list:
                # we keep calling the class_order method via recursion until all classes and their dependencies
                # have been inspected
                ordered_class = self.get_task_order(task=dependency)
                task_list.extend(ordered_class)
            task_list.append(task)
        else:
            task_list.append(task)
        return task_list

    @staticmethod
    def get_distinct_task_order(ordered_tasks):
        """
        Given a list of ordered tasks, removes any duplicates so that we have a list of distinct tasks
        :return: list of distinct tasks
        """
        assert isinstance(ordered_tasks, list)
        distinct_list = []
        for task in ordered_tasks:
            if task not in distinct_list:
                distinct_list.append(task)
        return distinct_list

    def run_tasks(self, **kwargs):
        """
        Runs the tasks (instantiates classes with optional and kwargs) in a ordered fashion
        :return: number of tasks ran
        """
        task_list = []
        for task in self.get_tasks():
            task_list.extend(self.get_task_order(task=task))
        tasks = self.get_distinct_task_order(ordered_tasks=task_list)
        for task in tasks:
            try:
                task(**kwargs).run()
            except Exception as error:
                raise error
        number_of_tasks_ran = len(tasks)
        print "{task_number} task(s) ran successfully".format(task_number=number_of_tasks_ran)
        return number_of_tasks_ran
