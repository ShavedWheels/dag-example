import unittest
import task_runner
import mocked_classes as md
import empty_mocked_classes as empty_module


class TestDependencyRunner(unittest.TestCase):

    def setUp(self):
        self.runner = task_runner.TaskRunner(module=md)

    def test_get_tasks(self):
        for class_name in self.runner.get_tasks():
            self.assertIn(class_name.__name__, dir(md))

    def test_get_tasks_with_empty_module(self):
        self.runner.module = empty_module
        self.assertRaises(Exception, self.runner.get_tasks)

    def test_get_tasks_with_incorrect_dependency_name(self):
        self.runner.module = empty_module
        self.assertRaises(Exception, self.runner.get_tasks)

    def test_has_dependency_with_dependencies(self):
        orders = self.runner.task_has_dependencies(obj=md.B)
        order_item = self.runner.task_has_dependencies(obj=md.C)
        self.assertTrue(orders)
        self.assertTrue(order_item)

    def test_has_dependency_with_no_dependencies(self):
        dates = self.runner.task_has_dependencies(obj=md.A)
        self.assertFalse(dates)

    def test_get_task_order(self):
        class_order = self.runner.get_task_order(task=md.C)
        expected = [md.A, md.A, md.B, md.D, md.C]
        self.assertEqual(class_order, expected)

    def test_get_distinct_task_order(self):
        expected = [md.A, md.B, md.D, md.C, md.F]
        task_list = [md.A, md.A, md.B, md.B,  md.D, md.D, md.D, md.C, md.C, md.F]
        self.assertEqual(self.runner.get_distinct_task_order(ordered_tasks=task_list), expected)

    def test_run_tasks(self):
        self.assertEqual(self.runner.run_tasks(), 6)

if __name__ == '__main__':
    unittest.main()
