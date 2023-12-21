import pytest
import random

from requests import HTTPError
from config import SERVER_URL
from Tasks.tasks import create_task, modify_task, mark_task_completed, mark_task_incompleted, delete_task
from Utils.task_verifier import TaskVerifier


@pytest.fixture(scope="function")
def task_obj():
    name="Playing a game"
    description="go and play video games with my friends"
    task_id = create_task(task=name, description=description)
    new_task = {
        "ID": task_id,
        "Name": name,
        "Description": description
        }
    yield new_task
    delete_task(task_id)
   

class TestTasks:
 
    def test_create_task(self, task_obj):
        # a test to create a task and verify it
        TaskVerifier.verify_check_task_exists(task_id=task_obj["ID"])
            
    def test_modify_task(self, task_obj):
        # a test to create and modify a task then verify it
        new_description = "Playing Elden Ring"
        modify_task(task_id=task_obj["ID"], name=task_obj["Name"], description=new_description)
        TaskVerifier.verify_task_modified(task_id=task_obj["ID"], name=task_obj["Name"], description=new_description)

    def test_mark_complete(self, task_obj):
        # a test to mark a task complete and verify it
        mark_task_completed(task_id=task_obj["ID"])
        TaskVerifier.verify_task_was_marked(task_id=task_obj["ID"],marked=True)

    def test_mark_incomplete(self, task_obj):
        # a test to mark a task incomplete and verify it
        mark_task_incompleted(task_id=task_obj["ID"])
        TaskVerifier.verify_task_was_marked(task_id=task_obj["ID"], marked=False)

    def test_task_delete(self, task_obj):
        # a test to delete a task and verify it
        delete_task(task_id=task_obj["ID"])
        TaskVerifier.verify_task_was_deleted(task_id=task_obj["ID"])

    def test_modify_none_existing_task(self):
        # a test to modify none esisting task
        random_id = random.randrange(900,1000)
        with pytest.raises(HTTPError):
                modify_task(task_id=random_id, name="Sleeping", description="Getting a full night sleep")
 
    def test_tast_lifecycle(self):

        # creat a task
        task_id = create_task(task="Movie", description="Watching the movie Fight Club")

        # modify the task and cheack if was created
        modify_task(task_id=task_id, name="Eating", description="Eating a pizza for lunch")
        TaskVerifier.verify_task_modified(task_id=task_id,name="Eating",description="Eating a pizza for lunch")

        # mark completed and check if it was marked
        mark_task_completed(task_id=task_id)
        TaskVerifier.verify_task_was_marked(task_id=task_id, marked=True)

        # mark incomplete and check if it was marked
        mark_task_incompleted(task_id=task_id)
        TaskVerifier.verify_task_was_marked(task_id=task_id, marked=False)

        # delete the task and cheack if it was deleated
        delete_task(task_id=task_id)
        TaskVerifier.verify_task_was_deleted(task_id=task_id)
