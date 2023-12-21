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
            Returns:
                    req the request response
        """
        suffix = TaskVerifier.suffix + str(task_id)
        req = HttpRequest.http_req(suffix=suffix, method=TaskVerifier.method)
        return req

    def verify_task_modified(task_id, name, description):
        """The function takes an id
            and then checking if it was modified.

             Args:
                task_id (str): the id of the task we want to check.
        """
        req = TaskVerifier().get_req(task_id)
        req.raise_for_status()
        values = req.json().values()
        assert isinstance(req.json(), dict), "Request didn't return as a dictionary."
        assert name and description in values, "The task's data wasn't modified."

    def verify_task_was_marked(task_id, marked):
        """The function takes an id
            and then checking if it was marked completed or incomplete.

             Args:
                task_id (str): the id of the task we want to check.
                marked (bool): True if its a completed task, False if its incomplete.
        """
        req = TaskVerifier().get_req(task_id)
        req.raise_for_status()

        if marked:
            assert True in req.json().values()
        else:
            assert False in req.json().values()
    
    def verify_check_task_exists(task_id):
        """The function checking if
            a task was created by checking it's id we got from the request.

            Args:
                 task_id (str): id to check if exists
         """
        req = TaskVerifier().get_req(task_id)
        req.raise_for_status()
        assert "ID" in req.json() , "Request didn't return as a dictionary with ID, Task wasn't found"
    
    def verify_task_was_deleted(task_id):
        """The function checking if
            a task was deleated.

            Args:
             task_id (str): id to check if exists
        """
        req = TaskVerifier().get_req(task_id)
        assert "ID" not in req.json() , "Request return a task, Task wasn't deleated"
