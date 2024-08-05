import proto_classes.vacancy_service_pb2 as vacancy_service_pb2
import proto_classes.vacancy_pb2 as vacancy__pb2

from proto_classes.vacancy_service_pb2_grpc import VacancyServiceStub
from google.protobuf.json_format import MessageToDict

from classes.channel import Channel

class Vacancy(Channel):
    def __init__(self, host, interceptor):
        super().__init__(host, VacancyServiceStub, interceptor=interceptor)

    def create_vacancy(self, division, title, description, country):
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
        response = self.stub.GetVacancy(
            vacancy_service_pb2.VacancyRequest(
                Id=id
            )
        )
        return MessageToDict(response)
    
    def delete_vacancy(self, id):
        response = self.stub.DeleteVacancy(
            vacancy_service_pb2.VacancyRequest(
                Id=id
            )
        )
        return MessageToDict(response)
    
    def list_vacancies(self, page, limit):
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