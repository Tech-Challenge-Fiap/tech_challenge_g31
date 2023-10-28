from flask_restful import Resource
from system.application.dto.requests.client_request import CreateClientRequest
from system.application.dto.responses.client_response import (
    CreateClientResponse,
    GetAllClientsResponse,
    GetClientByCPFResponse,
)
from system.application.exceptions.client_exceptions import ClientDoesNotExistError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.repositories.client_repository import (
    ClientRepository,
)


class CreateClientUseCase(UseCase, Resource):
    def execute(request: CreateClientRequest) -> CreateClientResponse:
        """
        Create client
        """
        client = ClientEntity(**request.model_dump())
        try:
            response = ClientRepository.create_client(client)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        return CreateClientResponse(response.model_dump())


class GetClientByCPFUseCase(UseCase, Resource):
    def execute(cpf: str) -> GetClientByCPFResponse:
        """
        Get client by cpf
        """
        try:
            client = ClientRepository.get_client_by_cpf(cpf)
        except NoObjectFoundError:
            raise ClientDoesNotExistError
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        return GetClientByCPFResponse(client.model_dump())


class GetAllClientsUseCase(UseCaseNoRequest, Resource):
    def execute() -> GetAllClientsResponse:
        """
        Get clients with filters
        """
        try:
            response = ClientRepository.get_all_clients()
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        return GetAllClientsResponse(response)
