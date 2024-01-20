from flask_restful import Resource
from system.application.dto.requests.client_request import CreateClientRequest
from system.application.dto.responses.client_response import (
    CreateClientResponse,
    GetAllClientsResponse,
    GetClientByCPFResponse,
)
from system.application.exceptions.client_exceptions import ClientDoesNotExistError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.ports.client_port import ClientPort
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.client import ClientEntity
from system.application.exceptions.repository_exceptions import NoObjectFoundError, DataRepositoryExeption


class CreateClientUseCase(UseCase, Resource):
    def execute(request: CreateClientRequest, client_repository: ClientPort) -> CreateClientResponse:
        """
        Create client
        """
        client = ClientEntity(**request.model_dump())
        try:
            response = client_repository.create_client(client)
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return CreateClientResponse(response.model_dump())


class GetClientByCPFUseCase(UseCase, Resource):
    def execute(cpf: str, client_repository: ClientPort) -> GetClientByCPFResponse:
        """
        Get client by cpf
        """
        try:
            client = client_repository.get_client_by_cpf(cpf)
        except NoObjectFoundError:
            raise ClientDoesNotExistError
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return GetClientByCPFResponse(client.model_dump())


class GetAllClientsUseCase(UseCaseNoRequest, Resource):
    def execute(client_repository: ClientPort) -> GetAllClientsResponse:
        """
        Get clients with filters
        """
        try:
            response = client_repository.get_all_clients()
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return GetAllClientsResponse(response)
