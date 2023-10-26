from flask_restful import Resource
from system.application.dto.requests.client_request import CreateClientRequest
from system.application.dto.responses.client_response import (
    CreateClientResponse,
    GetAllClientsResponse,
    GetClientByCPFResponse,
)
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.client_exceptions import (
    ClientDoesNotExistError,
)

from system.infrastructure.adapters.database.repositories.client_repository import (
    ClientRepository,
)


class CreateClientUseCase(Resource):
    def execute(request: CreateClientRequest) -> CreateClientResponse:
        """
        Create client
        """
        client = ClientEntity(**request.model_dump())
        response = ClientRepository.create_client(client)

        return CreateClientResponse(response.model_dump())


class GetClientByCPFUseCase(Resource):
    def execute(cpf: str) -> GetClientByCPFResponse:
        """
        Get client by cpf
        """
        client = ClientRepository.get_client_by_cpf(cpf)
        if not client:
            raise ClientDoesNotExistError
        return GetClientByCPFResponse(client.model_dump())


class GetAllClientsUseCase(Resource):
    def execute() -> GetAllClientsResponse:
        """
        Get clients with filters
        """
        response = ClientRepository.get_all_clients()
        return GetAllClientsResponse(response)
