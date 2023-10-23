from typing import List
from flask_restful import Resource
from psycopg2 import IntegrityError
from system.application.dto.requests.client_request import CreateClientRequest
from system.application.dto.responses.client_response import CreateClientResponse, GetAllClientsResponse, GetClientByCPFResponse
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.client_exceptions import ClientAlreadyExistsError, ClientDoesNotExistError

from system.infrastructure.adapters.database.repositories.client_repository import ClientRepository

class CreateClientUseCase(Resource):
    def execute(
        request: CreateClientRequest
    ) -> CreateClientResponse:
        """
        Create client
        """
        client = ClientEntity(**request.model_dump())
        try:
            response = ClientRepository.create_client(client)
        except IntegrityError as err:
            raise ClientAlreadyExistsError(str(err))
       
        return CreateClientResponse(response.model_dump())

class GetClientByCPFUseCase(Resource):
    def execute(
        cpf: str
    ) -> GetClientByCPFResponse:
        """
        Get client by cpf
        """
        try:
            response = ClientRepository.get_client_by_cpf(cpf)
        except IntegrityError as err:
            raise ClientDoesNotExistError(str(err))
       
        return GetClientByCPFResponse(response.model_dump())
    
class GetAllClientsUseCase(Resource):
    def execute(
    ) -> GetAllClientsResponse:
        """
        Get clients with filters
        """
        try:
            response = ClientRepository.get_all_clients()
        except:
            raise IntegrityError
       
        return GetAllClientsResponse(response)