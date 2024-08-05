from locust import User

from interceptor import Interceptor
from classes.auth import Auth
from classes.vacancy import Vacancy

class GrpcUser(User):
    abstract = True

    def __init__(self, parent, host, email, password, environment):
        super().__init__(environment)
        self.interceptor = Interceptor(environment=environment)
        self.email = email
        self.host = host
        self.password = password
        self.auth_obj = None

        self.setup()

    def setup(self):
        # Make channels here
        self.authentication = Auth(self.host, self.email, self.password, self.interceptor)
        self.vacancy = Vacancy(self.host, self.interceptor)

    def auth(self):
        # Maybe send this into the interceptor
        # Or into the grpc_user to renew after each call
        if not self.auth_obj:
            response = self.authentication.sign_in_user(self.email, self.password)
            self.auth_obj = response
        return self.auth_obj
    
    def create_vacancy(self, division, title, description, country):
        return self.request(self.vacancy.create_vacancy, (division, title, description, country), True)
    
    def edit_vacancy(self, vacancy, division, title, description, country):
        id = vacancy["vacancy"]["Id"]
        return self.request(self.vacancy.edit_vacancy, (id, division, title, description, country), True)
    
    def get_vacancy(self, id):
        return self.request(self.vacancy.get_vacancy, (id,), True)
    
    def delete_vacancy(self, id):
        return self.request(self.vacancy.delete_vacancy, (id,), True)
    
    def list_vacancies(self, page, limit):
        return self.request(self.vacancy.list_vacancies, (page, limit), True)

    def request(self, method, args, auth):
        if auth:
            self.auth()
        return method(*args)
