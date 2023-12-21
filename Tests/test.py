from config import SERVER_URL
from Tasks.tasks import CreateTask, ModifyTask, ChangeTaskStatus, DeleteTask
from Utils.logging_utils import logging
from Utils.task_verifier import TaskVerifier


class TestFlow:
    def __init__(self):
        self.task_ids_list = []

    def test_flow(self):
        try:
            logging.info("Starts testing with URL: [{}]".format(SERVER_URL))

            # Testing if the task was created
            self.test_create_task(name="Playing a game", new_description="go and play video games with my friends")

            # Creating a task to modify
            self.test_modify_task(name="Eating", new_description="Eating a pizza for lunch")

            # Creating a task to delete
            self.test_task_delete(name="Watch a movie", new_description="Watch Fight Club")

            # Creating a task to mark completed
            self.test_mark_complete(name="Visit family", new_description="Visit my grandparents")

            # Creating a task to mark incomplete
            self.test_mark_incomplete(name="Exercise", new_description="Go to the gym")

        except Exception:
            logging.exception("\nGENERAL FLOW FAILED\n")
        else:
            logging.info("All tests have been deployed\n")
        finally:
            self.delete_tasks()

    def test_create_task(self, name="new task", new_description=None):
        try:
            task_id = CreateTask().create_task(task=name, description=new_description)
            TaskVerifier.verefiy_check_task_exists(task_id=task_id)
            self.task_ids_list.append(task_id)
        except Exception as err:
            logging.exception(str(err))        

    def test_modify_task(self, name, new_description):
            try:
                task_id = CreateTask().create_task(task=name, description=new_description)
                ModifyTask().modify_task(task_id, name=name, description="Eating fried rice for lunch")
                TaskVerifier.verefiy_task_modified(task_id=task_id, old_name=name,old_description=new_description)
                self.task_ids_list.append(task_id)
            except Exception as err:
                logging.exception(str(err))

    def test_mark_complete(self, name, new_description):
        try:
            task_id = CreateTask().create_task(task=name, description=new_description)
            ChangeTaskStatus().mark_task_completed(task_id)
            TaskVerifier.verefiy_task_was_marked(task_id=task_id,marked=True)
            self.task_ids_list.append(task_id)
        except Exception as err:
            logging.exception(str(err))

    def test_mark_incomplete(self, name, new_description):
        try:
            task_id = CreateTask().create_task(task=name, description=new_description, completed=True)
            ChangeTaskStatus().mark_task_incompleted(task_id)
            TaskVerifier.verefiy_task_was_marked(task_id=task_id, marked=False)
            self.task_ids_list.append(task_id)
        except Exception as err:
            logging.exception(str(err))

    def test_task_delete(self, name, new_description):
        try:
            task_id = CreateTask().create_task(task=name, description=new_description)
            DeleteTask().delete_task(task_id)
        except Exception as err:
            logging.exception(str(err))


    def delete_tasks(self):
        DeleteTask().delete_tasks(self.task_ids_list)
