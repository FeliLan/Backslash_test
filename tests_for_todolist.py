import json
import logging
import os
import sys
import requests

""" Global param """
task_ids_list = list()  # A list to add all the new task I'll create and then remove them.
server_url = ''


def http_req(method, suffix, headers=None, body=None):
    """General http req, send the info of what you want to request
        and pass it to the server for handling.

    Args:
        method (str): Method of the function ("Get"/"Post"/"Put")
        suffix (str): suffix to add to server_url
        headers (dict): header to add to request. default {}
        body (dict): body (data) to add to request

    Returns:
        Union[dict, list]: Response.json() object
    """
    if headers is None:
        headers = {"Content-Type": "application/json"}
    url = "{}{}".format(server_url, suffix)
    req = ""
    try:
        if body:
            body = json.dumps(body)
        req = requests.request(method=method, url=url, headers=headers, data=body)
        assert 300 > req.status_code >= 200
        return req.json()
    except ValueError as exception:
        msg = "Could not parse json from url [{}]\nHeaders [{}]\nBody: [{}]\nText: [{}]".format(
            url, headers, body, req.text if req else "")
        logging.exception(msg)
        raise exception
    except AssertionError:
        msg = "Got unexpected status code [{}]".format(req.status_code)
        logging.exception(msg)
        raise AssertionError


def create_task(task="new task", description= None, completed=False):
    """Create a new task

        Args:
            task (str): task discretion
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
    task_id = http_req(suffix=suffix, method=method, body=body).get("ID")
    logging.info("New task created with id [{}]".format(task_id))
    return task_id


class ListTasks:
    suffix = "api/todo"
    method = "get"

    def list_tasks(self):
        """Getting the list of tasks.

            Returns:
                dict: Returns the request we got back.
            """
        func_name = "test_list_tasks"
        logging.info("Starting {}".format(func_name))
        req = http_req(suffix=self.suffix, method=self.method)
        assert req, "Got no tasks in the task list"
        logging.info("Task [{}] passed".format(func_name))
        return req


class ModifyTask:
    suffix = "api/todo/{}"
    method = "put"

    def modify_task(self, task_id, name, description):
        """The function send a request
            to modify the task.

            Args:
                 task_id (str): the id of the task we want to modify

        """
        logging.info("Modifying task id [{}]".format(task_id))
        suffix = self.suffix.format(task_id)
        try:
            body = {
                "Name": name,
                "Description": description
            }
            http_req(suffix=suffix, method=self.method, body=body)
        except AssertionError:
            logging.error("Failed to modify task id [{}]".format(task_id))
        logging.info("Task [{}] was modified".format(task_id))


class ChangeTaskStatus:
    suffix = "api/todo/{}"
    method = "put"

    def mark_task_completed(self, task_id):
        """The function takes an id
            of a task then marking it completed.

             Args:
                task_id (str): the id of the task we want to mark.
        """
        func_name = "mark_task_completed"
        logging.info("Starting {}".format(func_name))
        suffix = self.suffix.format(task_id)
        try:
            body = {
                "Is_complete": True
            }
            http_req(suffix=suffix, method=self.method, body=body)
        except AssertionError:
            logging.error("No task with id {} to mark completed".format(task_id))
            raise AssertionError
        logging.info("Task [{}] passed".format(func_name))

    def mark_task_incompleted(self, task_id):
        """The function takes an id
            of a task then marking it incompleted.

             Args:
                task_id (str): the id of the task we want to mark.
        """
        func_name = "mark_task_incompleted"
        logging.info("Starting {}".format(func_name))
        suffix = self.suffix.format(task_id)
        try:
            body = {
                "Is_complete": False
            }
            http_req(suffix=suffix, method=self.method, body=body)
        except AssertionError:
            logging.error("No task with id {} to mark incompleted".format(task_id))
            raise AssertionError
        logging.info("Task [{}] passed".format(func_name))


class TaskProperties:
    suffix = "api/todo/{}"
    method = "get"

    def get_req(self, task_id):
        """the function takes an id
            and getting it's request to help other function
            handle request much easier.

             Args:
                task_id (str): the id of the task we want to get.

             Returns:
                dict: return the request
        """
        suffix = self.suffix.format(task_id)
        req = http_req(self.method, suffix=suffix)
        return req

    def task_modified(self, task_id, old_name, old_description):
        """The function takes an id
            and then checking if it was modified.

             Args:
                task_id (str): the id of the task we want to check.

            Returns:
                return the request (dict)
        """
        func_name = "test_task_modified"
        logging.info("Starting {}".format(func_name))
        self.suffix += str(task_id)
        req = TaskProperties().get_req(task_id)
        values = req.values()
        assert isinstance(req, dict), "Request didn't return as a dictionary."
        assert old_name or old_description not in values, "The task's data wasn't modified."
        logging.info("Task [{}] passed".format(func_name))
        return req

    def task_was_marked(self, task_id, marked):
        """The function takes an id
            and then checking if it was marked completed or incomplete.

             Args:
                task_id (str): the id of the task we want to check.
                marked (bool): True if its a completed task, False if its incomplete.

             Returns:
                dict: return the request
        """
        func_name = "test_task_was_marked"
        logging.info("Starting {}".format(func_name))
        req = TaskProperties().get_req(task_id)
        try:
            if marked:
                assert True in req.values()
            else:
                assert False in req.values()
        except AssertionError:
            msg = "Couldn't find status [{}] for task_id [{}]".format(marked, task_id)
            raise AssertionError(msg)
        logging.info("Task [{}] passed".format(func_name))
        return req
    
    def check_task_exists(self, task_id):
        """The function checking if
            a task was created by checking it's id we got from the request.

            Args:
                 task_id (str): id to check if exists

            Returns:
                 str: return the the task_id
         """
        func_name = "check_task_exists"
        logging.info("Starting [{}] with task_id [{}]".format(func_name, task_id))
        self.suffix += str(task_id)
        
        req = TaskProperties().get_req(task_id)
        assert isinstance(req, dict), "Request didn't return as a dictionary, Task wasn't found"

        task_list = ListTasks().list_tasks()
        exist = False
        for task in task_list:
            if task["ID"] == task_id:
                exist = True
        if not exist:
            msg = "Got no task [{}] in the list".format(task_id)
            raise ValueError(msg)
        logging.info("Task [{}] passed".format(func_name))
        return task_id


class DeleteTask:
    suffix = "api/todo/{}"
    method = "DELETE"

    def delete_task(self, task_id):
        """The function takes an id
            and then deleting the task.

             Args:
                task_id (str): the id of the task we want to delete.
        """
        logging.info("Deleting task id [{}]".format(task_id))
        suffix = self.suffix.format(task_id)
        try:
            http_req(suffix=suffix, method=self.method)
        except AssertionError:
            logging.error("No task with id {} to delete".format(task_id))
            raise AssertionError
        logging.info("Task [{}] was deleted".format(task_id))

    def check_task_deleted(self, task_id):
        """The function checking if
            the task was deleted.

            Args:
                 task_id (str): id to check if deleted
         """
        func_name = "check_task_deleted"
        logging.info("Starting [{}] with task_id [{}]".format(func_name, task_id))
        task_list = ListTasks().list_tasks()
        exist = False
        for task in task_list:
            if task["ID"] == task_id:
                exist = True
        if exist:
            msg = "Task [{}] wasn't deleted".format(task_id)
            raise ValueError(msg)
        logging.info("Task [{}] passed".format(func_name))



def test_mark_complete(name, new_description):
    try:
        # Create a Task
        task_id = create_task(task=name, description=new_description)
        # Mark task completed
        ChangeTaskStatus().mark_task_completed(task_id)
        # Check if task completed
        TaskProperties().task_was_marked(task_id, True)
        # Add to list
        task_ids_list.append(task_id)
    except Exception as err:
        logging.exception(str(err))


def test_mark_incomplete(name, new_description):
    try:
        # Create a Task
        task_id = create_task(task=name, description=new_description, completed=True)
        # Mark task incomplete
        ChangeTaskStatus().mark_task_incompleted(task_id,)
        # Check if task incomplete
        TaskProperties().task_was_marked(task_id, False)
        # Add to list
        task_ids_list.append(task_id)
    except Exception as err:
        logging.exception(str(err))


def test_task_delete(name, new_description):
    try:
        # Create a Task
        task_id = create_task(task=name, description=new_description,)
        # Delete the task
        DeleteTask().delete_task(task_id)
        # Check if task deleted
        DeleteTask().check_task_deleted(task_id)
    except Exception as err:
        logging.exception(str(err))


def test_modify_task(name, new_description):
    try:
        # Create a Task
        task_id = create_task(task=name,description=new_description)
        # Modify task
        ModifyTask().modify_task(task_id,name=name,description="Eating fried rice for lunach")
        # Check if changed
        TaskProperties().task_modified(task_id, old_name=name, old_description=new_description)
        # Add to list
        task_ids_list.append(task_id)
    except Exception as err:
        logging.exception(str(err))


def test_create_task(name="new task", new_description=None):
    try:
        # Create a Task
        task_id = create_task(task=name,description=new_description)
        # Check if created
        TaskProperties().check_task_exists(task_id)
        # Add to list
        task_ids_list.append(task_id)
    except Exception as err:
        logging.exception(str(err))


def delete_tasks():
    """
    The function deletes all the task,
    if all test ran with no errors.
    """
    task_deleter = DeleteTask().delete_task

    logging.info("Finish all tests, cleaning server")
    for task_id in task_ids_list:
        try:
            task_deleter(task_id)
        except AssertionError:  # Pass on non-existing task
            pass
    logging.info("Server cleaned")


def test_flow():
    """ Running test functions one by one
    """
    try:

        # Testing if the task was created
        test_create_task(name="Playing a game", new_description="go and play video games with my friends")

        # Creating a task to modify
        test_modify_task(name="Eating", new_description="Eating a pizza for lunach")

        # Creating a task to delete
        test_task_delete(name="Watch a movie", new_description="Watch Fight Clab")

        # Creating a task to mark completed
        test_mark_complete(name="Visit family", new_description="Visit my granddparants")

        # Creating a task to mark incomplete
        test_mark_incomplete(name="Exercise", new_description="Go to the gym")

        delete_tasks()

    except Exception:
        logging.exception("\nGENERAL FLOW FAILED\n")


def configure_logging():
    """
    settings for the log file,
    what to write to it,
    and what format to use.
    """
    is_logging_level_set = True
    try:
        logging_level = sys.argv[2]
        if logging_level not in (
                logging.INFO, logging.DEBUG, logging.WARNING,
                logging.ERROR, logging.CRITICAL, logging.FATAL
        ):
            raise IndexError
    except IndexError:
        logging_level = logging.INFO
        is_logging_level_set = False
    finally:
        if not is_logging_level_set:
            logging_level = logging.INFO

    formatter = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        filemode="a",
        filename="backslash.log",
        level=logging_level,
        format=formatter
    )


def main():
    """
    The main function, activates the log, and receiving the URL
    to run the tests on.
    """

    try:
        global server_url
        configure_logging()
        server_url = sys.argv[1]  # type: str
        server_url = server_url if server_url.endswith('/') else server_url + '/'
        logging.info("Starts testings with url: [{}]".format(server_url))
        test_flow()
        logging.info("All tests have been deployed\n\n")
    except IndexError as e:
        file_name = os.path.basename(__file__)
        logging.error("Server url did not supplied\n run 'python {} <SERVER URL>'\n\n".format(file_name))


if __name__ in ('__main__', 'main'):
    main()
