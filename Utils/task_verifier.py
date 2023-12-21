from Utils.logging_utils import logging
from Utils.http_request import HttpRequest

class TaskVerifier:
    suffix = "api/todo/"
    method = "get"

    def get_req(self, task_id):
        """the function takes an id
            and getting it's request to help other function
            handle request much easier.

             Args:
                task_id (str): the id of the task we want to get.
        """
        suffix = TaskVerifier.suffix + str(task_id)
        req = HttpRequest.http_req(suffix=suffix, method=TaskVerifier.method)
        return req

    def verefiy_task_modified(task_id, old_name, old_description):
        """The function takes an id
            and then checking if it was modified.

             Args:
                task_id (str): the id of the task we want to check.
        """
        func_name = "test_task_modified"
        logging.info("Starting {}".format(func_name))
        req = TaskVerifier().get_req(task_id)
        values = req.values()
        assert isinstance(req, dict), "Request didn't return as a dictionary."
        assert old_name or old_description not in values, "The task's data wasn't modified."
        logging.info("Task [{}] passed".format(func_name))
        return req

    def verefiy_task_was_marked(task_id, marked):
        """The function takes an id
            and then checking if it was marked completed or incomplete.

             Args:
                task_id (str): the id of the task we want to check.
                marked (bool): True if its a completed task, False if its incomplete.
        """
        func_name = "test_task_was_marked"
        logging.info("Starting {}".format(func_name))
        req = TaskVerifier().get_req(task_id)
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
    
    def verefiy_check_task_exists(task_id):
        """The function checking if
            a task was created by checking it's id we got from the request.

            Args:
                 task_id (str): id to check if exists
         """
        func_name = "check_task_exists"
        logging.info("Starting [{}] with task_id [{}]".format(func_name, task_id))
        req = TaskVerifier().get_req(task_id)
        assert "ID" in req.keys() , "Request didn't return as a dictionary with ID, Task wasn't found"
        logging.info("Task [{}] passed".format(func_name))