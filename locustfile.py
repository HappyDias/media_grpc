import time
import json
import gevent
import grpc
import random
import string

from locust import task, constant, events
from locust.exception import LocustError

from grpc_user import GrpcUser

# Users seem to need to exist on a file as a list here

with open('auth.json') as auth_file:
    user_creds = json.load(auth_file)

class TestUser(GrpcUser):
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

        super().__init__(self, host, email, password, *args, **kwargs)
        gevent.spawn(self.list_vacancies_task, args[0])

    def list_vacancies_task(self, environment):
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
