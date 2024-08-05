import proto_classes.vacancy_service_pb2 as vacancy_service_pb2
import proto_classes.vacancy_pb2 as vacancy__pb2

from proto_classes.vacancy_service_pb2_grpc import VacancyServiceStub
from google.protobuf.json_format import MessageToDict

from classes.channel import Channel

class Vacancy(Channel):
    """
    Initializes a Vacancy object.
    Args:
        host (str): The host of the Vacancy service.
        interceptor: The interceptor for the Vacancy service.
    """
    def __init__(self, host, interceptor):
        """
        Initializes a new instance of the Vacancy class.

        Args:
            host (str): The host of the Vacancy.
            interceptor: The interceptor for the Vacancy.

        Returns:
            None
        """
        super().__init__(host, VacancyServiceStub, interceptor=interceptor)

    def create_vacancy(self, division, title, description, country):
        """
        Creates a new vacancy.

        Args:
            division (str): The division of the vacancy.
            title (str): The title of the vacancy.
            description (str): The description of the vacancy.
            country (str): The country of the vacancy.

        Returns:
            dict: A dictionary containing the response message.
        """
        response = self.stub.CreateVacancy(
            vacancy_service_pb2.rpc__create__vacancy__pb2.CreateVacancyRequest(
                Division=division,
                Title=title,
                Description=description,
                Country=country
            )
        )
        return MessageToDict(response)
    
    def edit_vacancy(self, id, division, title, description, country):
        """
        Edit a vacancy with the given parameters.

        Args:
            id (int): The ID of the vacancy to be edited.
            division (str): The division of the vacancy.
            title (str): The title of the vacancy.
            description (str): The description of the vacancy.
            country (str): The country of the vacancy.

        Returns:
            dict: A dictionary containing the updated vacancy.
        """
        response = self.stub.UpdateVacancy(
            vacancy_service_pb2.rpc__update__vacancy__pb2.UpdateVacancyRequest(
                Id=id,
                Division=division,
                Title=title,
                Description=description,
                Country=country,
                Views=10
            )
        )
        return MessageToDict(response)
    
    def get_vacancy(self, id):
        """
        Retrieves a vacancy by its ID.

        Args:
            id (int): The ID of the vacancy.

        Returns:
            dict: A dictionary representation of the vacancy response.
        """
        response = self.stub.GetVacancy(
            vacancy_service_pb2.VacancyRequest(
                Id=id
            )
        )
        return MessageToDict(response)
    
    def delete_vacancy(self, id):
        """
        Deletes a vacancy with the given ID.

        Parameters:
            id (int): The ID of the vacancy to be deleted.

        Returns:
            dict: A dictionary representing the response message. Should be a boolean value
        """
        response = self.stub.DeleteVacancy(
            vacancy_service_pb2.VacancyRequest(
                Id=id
            )
        )
        return MessageToDict(response)
    
    def list_vacancies(self, page, limit):
        """
        Retrieves a list of vacancies.

        Args:
            page (int): The page number of the vacancies to retrieve.
            limit (int): The maximum number of vacancies to retrieve per page.

        Returns:
            list: A list of dictionaries representing the retrieved vacancies.
        """
        page=page,
        limit=limit
        vacancies = []
        response = self.stub.GetVacancies(
            vacancy_service_pb2.GetVacanciesRequest(
                page=5,
                limit=10
            )
        )
        for vacancy in response:
            vacancies.append(MessageToDict(vacancy))
        return vacancies