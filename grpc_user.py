from locust import User

from interceptor import Interceptor
from classes.auth import Auth
from classes.vacancy import Vacancy

class GrpcUser(User):
    """
    GrpcUser class represents a gRPC user with authentication and various methods for interacting with vacancies.
    Attributes:
        abstract (bool): Abstract class for locust purposes.
    Methods:
        __init__(self, parent, host, email, password, environment): Initializes a GrpcUser object.
        setup(self): Sets up the gRPC channels.
        auth(self): Authenticates the user and returns the authentication object.
        create_vacancy(self, division, title, description, country): Creates a new vacancy.
        edit_vacancy(self, vacancy, division, title, description, country): Edits an existing vacancy.
        get_vacancy(self, id): Retrieves a vacancy by its ID.
        delete_vacancy(self, id): Deletes a vacancy by its ID.
        list_vacancies(self, page, limit): Lists vacancies with pagination support.
        request(self, method, args, auth): Makes a request to a gRPC method with optional authentication.
    Note:
        - The GrpcUser class is a subclass of the Locust User class to be used for load testing.
        - The GrpcUser class requires the host, email, password, and environment parameters to be initialized.
        - The setup method initializes the authentication and vacancy channels. Update when more channels required
    """
    abstract = True

    def __init__(self, host, email, password, environment):
        """
        Initializes a new instance of the `grpc_user` class.
        Args:
            host: The host address.
            email: The email address.
            password: The password.
            environment: The environment.
        Returns:
            None
        """
        super().__init__(environment)
        self.interceptor = Interceptor(environment=environment)
        self.email = email
        self.host = host
        self.password = password
        self.auth_obj = None

        self.setup()

    def setup(self):
        """
        Sets up the necessary channels for communication.

        Parameters:
            None

        Returns:
            None
        """
        # Make channels here
        self.authentication = Auth(self.host, self.email, self.password, self.interceptor)
        self.vacancy = Vacancy(self.host, self.interceptor)

    def auth(self):
        """
        Authenticates the user by signing in with the provided email and password.

        Returns:
            The authentication object for the user.
        """
        # Maybe send this into the interceptor
        # Or into the grpc_user to renew after each call
        if not self.auth_obj:
            response = self.authentication.sign_in_user(self.email, self.password)
            self.auth_obj = response
        return self.auth_obj
    
    def create_vacancy(self, division, title, description, country):
        """
        Creates a vacancy with the given parameters.

        Args:
            division (str): The division of the vacancy.
            title (str): The title of the vacancy.
            description (str): The description of the vacancy.
            country (str): The country of the vacancy.

        Returns:
            The vacancy as a python dict.
        """
        return self.request(self.vacancy.create_vacancy, (division, title, description, country), True)
    
    def edit_vacancy(self, vacancy, division, title, description, country):
        """
        Edit a vacancy with the given parameters.

        Parameters:
        - vacancy (dict): The vacancy to be edited.
        - division (str): The division of the vacancy.
        - title (str): The new title of the vacancy.
        - description (str): The new description of the vacancy.
        - country (str): The new country of the vacancy.

        Returns:
        - The edited vacancy as a python dict.
        """
        id = vacancy["vacancy"]["Id"]
        return self.request(self.vacancy.edit_vacancy, (id, division, title, description, country), True)
    
    def get_vacancy(self, id):
        """
        Retrieves a vacancy with the given ID.

        Parameters:
        - id (int): The ID of the vacancy to retrieve.

        Returns:
        - object: The vacancy object as a python dict.

        """
        return self.request(self.vacancy.get_vacancy, (id,), True)
    
    def delete_vacancy(self, id):
        """
        Deletes a vacancy with the given ID.

        Parameters:
        - id (int): The ID of the vacancy to delete.

        Returns:
        - bool: True if the vacancy was successfully deleted, False otherwise.
        """
        return self.request(self.vacancy.delete_vacancy, (id,), True)
    
    def list_vacancies(self, page, limit):
        """
        Retrieves a list of vacancies.

        Args:
            page (int): The page number of the vacancies.
            limit (int): The maximum number of vacancies to retrieve per page.

        Returns:
            list: A list of vacancies.

        Raises:
            None
        """
        return self.request(self.vacancy.list_vacancies, (page, limit), True)

    def request(self, method, args, auth):
        """
        Sends a request to the server. Can handle authentication

        Args:
            method: The method to be called.
            args: The arguments to be passed to the method.
            auth: A boolean indicating whether authentication is required.

        Returns:
            The result of the method call.
        """
        if auth:
            self.auth()
        return method(*args)
