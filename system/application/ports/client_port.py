from abc import abstractmethod
from typing import List
from system.application.dto.requests.client_request import ClientPayload

from system.domain.entities.client import ClientEntity


class ClientPort:
    @classmethod
    @abstractmethod
    def create_client(payload: ClientPayload) -> ClientEntity:
        """
        Method that creates a client
        """

    @classmethod
    @abstractmethod
    def get_client_by_cpf(cpf) -> ClientEntity:
        """
        Method thar gets a client by its cpf
        """

    @classmethod
    @abstractmethod
    def get_all_clients() -> List[ClientEntity]:
        """
        Method that gets all clients
        """
