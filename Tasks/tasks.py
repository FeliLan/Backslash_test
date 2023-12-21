from Utils.http_request import HttpRequest
from Utils.logging_utils import logging


class CreateTask:
    @staticmethod
    def create_task(task="new task", description=None, completed=False):
        """Create a new task with an api request with the info given.

            Args:
                task (str): task name
                discretion(str): task discretion
                completed (bool): if task completed

            Returns:
                str: task_id
        """
        logging.info("Creates a new task")
        suffix = "api/todo"
        method = "post"
        body = {
            "Name": task,
            "Description": description,
            "Is_complete": completed
        }
        task_id = HttpRequest.http_req(suffix=suffix, method=method, body=body).get("ID")
        logging.info("New task created with id [{}]".format(task_id))
        return task_id

class ModifyTask:
    @staticmethod
    def modify_task(task_id, name, description):
        """The function send a request
            to modify the task.

            Args:
                 task_id (str): the id of the task we want to modify
                 name (str): the name of the task
                 description (str): task discretion

        """
        logging.info("Modifying task id [{}]".format(task_id))
        suffix = "api/todo/{}".format(task_id)
        try:
            body = {
                "Name": name,
                "Description": description
            }
            HttpRequest.http_req(suffix=suffix, method="put", body=body)
        except AssertionError:
            logging.error("Failed to modify task id [{}]".format(task_id))
        logging.info("Task [{}] was modified".format(task_id))

class ChangeTaskStatus:
    @staticmethod
    def mark_task_completed(task_id):
        """The function takes an id
            of a task then marking it completed.

             Args:
                task_id (str): the id of the task we want to mark.
        """
        logging.info("Marking task id [{}] as completed".format(task_id))
        suffix = "api/todo/{}".format(task_id)
        try:
            body = {"Is_complete": True}
            HttpRequest.http_req(suffix=suffix, method="put", body=body)
        except AssertionError:
            logging.error("No task with id {} to mark completed".format(task_id))
            raise AssertionError

    @staticmethod
    def mark_task_incompleted(task_id):
        """The function takes an id
            of a task then marking it incompleted.

             Args:
                task_id (str): the id of the task we want to mark.
        """
        logging.info("Marking task id [{}] as incomplete".format(task_id))
        suffix = "api/todo/{}".format(task_id)
        try:
            body = {"Is_complete": False}
            HttpRequest.http_req(suffix=suffix, method="put", body=body)
        except AssertionError:
            logging.error("No task with id {} to mark incomplete".format(task_id))
            raise AssertionError

class DeleteTask:
    @staticmethod
    def delete_task(task_id):
        """The function takes an id
            and then deleting the task.

             Args:
                task_id (str): the id of the task we want to delete.
        """
        logging.info("Deleting task id [{}]".format(task_id))
        suffix = "api/todo/{}".format(task_id)
        try:
            HttpRequest.http_req(suffix=suffix, method="delete")
        except AssertionError:
            logging.error("No task with id {} to delete".format(task_id))
            raise AssertionError
        logging.info("Task [{}] was deleted".format(task_id))

    def delete_tasks(self, task_ids):
        logging.info("Finish all tests, cleaning server. Deleting tasks: {}".format(task_ids))
        for task_id in task_ids:
            try:
                self.delete_task(task_id)
            except AssertionError:  # Pass on non-existing task
                pass
        logging.info("Server cleaned \n \n")
