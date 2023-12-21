from Utils.http_request import HttpRequest


def create_task(task="new task", description=None, completed=False):
    """Create a new task with an api request with the info given.

        Args:
            task (str): task name
            discretion(str): task discretion
            completed (bool): if task completed

        Returns:
                req as as a Task
    """
    suffix = "api/todo"
    method = "post"
    body = {
        "Name": task,
        "Description": description,
        "Is_complete": completed
    }
    req = HttpRequest.http_req(suffix=suffix, method=method, body=body)
    req.raise_for_status()
    return req.json().get("ID")



def modify_task(task_id, name, description):
    """The function send a request
        to modify the task.

        Args:
                task_id (str): the id of the task we want to modify
                name (str): the name of the task
                description (str): task discretion

    """
    suffix = "api/todo/{}".format(task_id)
    body = {
        "Name": name,
        "Description": description
    }
    req = HttpRequest.http_req(suffix=suffix, method="put", body=body)
    req.raise_for_status()

def mark_task_completed(task_id):
    """The function takes an id
        of a task then marking it completed.

            Args:
            task_id (str): the id of the task we want to mark.
    """
    suffix = "api/todo/{}".format(task_id)
    body = {"Is_complete": True}
    req = HttpRequest.http_req(suffix=suffix, method="put", body=body)
    req.raise_for_status()


def mark_task_incompleted(task_id):
    """The function takes an id
        of a task then marking it incompleted.

            Args:
            task_id (str): the id of the task we want to mark.
    """
    suffix = "api/todo/{}".format(task_id)
    body = {"Is_complete": False}
    req = HttpRequest.http_req(suffix=suffix, method="put", body=body)
    req.raise_for_status()


def delete_task(task_id):
    """The function takes an id
        and then deleting the task.

            Args:
            task_id (str): the id of the task we want to delete.
    """
    suffix = "api/todo/{}".format(task_id)
    req = HttpRequest.http_req(suffix=suffix, method="delete")
