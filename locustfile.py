import time
import json
import gevent
import grpc
import random
import string

from locust import task, constant, events
from locust.exception import LocustError

from grpc_user import GrpcUser

# Users need to exist on a file as a list here
with open('auth.json') as auth_file:
    user_creds = json.load(auth_file)

class TestUser(GrpcUser):
    """
    A class representing a test user for the magic_media application.
    Attributes:
        wait_time (int): The wait time in seconds between tasks.
    Methods:
        __init__(*args, **kwargs): Initializes a TestUser instance.
        list_vacancies_task(environment): Performs the list vacancies task.
        user_test(): Performs the user test task.
    """
    wait_time = constant(30)
    
    def __init__(self, *args, **kwargs):
        # Get user credentials from list
        # if more users than creds spawn, use fake creds
        email = None
        password = None
        host = "vacancies.cyrextech.net:7823"
        if len(user_creds) == 0:
            email = "fake"
            password = "fake"
        else:
            obj = user_creds.pop()
            email = obj["email"]
            password = obj["password"]

        super().__init__(host, email, password, args[0])
        gevent.spawn(self.list_vacancies_task)

    def list_vacancies_task(self):
        """
        Task that lists vacancies at regular intervals.

        This task runs indefinitely and lists vacancies by calling the `list_vacancies` method.
        It sleeps for a specified interval and then retrieves a random number of vacancies from a random page.
        The time taken to retrieve the vacancies is measured and used to adjust the sleep interval for the next iteration.

        Parameters:
        - self: The instance of the class.

        Returns:
        None
        """
        to_sleep_interval = 45
        to_sleep = to_sleep_interval
        while True:
            time.sleep(to_sleep)
            limit = random.randint(1, 10)
            page = random.randint(1, 100)
            time_start = time.time()
            vacancies = self.list_vacancies(page, limit)
            time_end = time.time()
            to_sleep = to_sleep_interval - (time_end - time_start)

    @task
    def user_test(self):
        """
        This method performs a series of actions related to vacancy management.
        It creates a new vacancy with randomly generated title, description, division, and country.
        Then it edits the created vacancy by randomly changing the division and title.
        Next, it fetches the edited vacancy using its ID.
        Finally, it deletes the vacancy using its ID.

        Returns:
            None
        """
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        division = random.randint(0, 3)
        division_edited = random.randint(0, 3)
        country = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
        vacancy = self.create_vacancy(division, title, description, country)
        vacancy_update = self.edit_vacancy(vacancy, division_edited, f"{title}_edited", f"{title}_edited", f"{title}_edited")
        id_v = vacancy["vacancy"]["Id"]
        vacancy_fetch = self.get_vacancy(id_v)
        vacancy_delete = self.delete_vacancy(id_v) # maybe vacancy?

    # def on_start(self, *args, **kwargs):
    #     print("I AM STARTED", args, kwargs)
