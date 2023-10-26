from typing import List
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.client_exceptions import (
    ClientDoesNotExistError,
    ClientAlreadyExistsError,
)
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.client_model import ClientModel


class ClientRepository:
    @staticmethod
    def create_client(client: ClientEntity) -> ClientEntity:
        """Create client"""
        client_to_insert = ClientModel(**client.model_dump())
        try:
            db.session.add(client_to_insert)
            db.session.commit()
        except IntegrityError as ex:
            if isinstance(ex.orig, UniqueViolation):
                raise ClientAlreadyExistsError
            raise ex
        return ClientEntity(**client.model_dump())

    @staticmethod
    def get_client_by_cpf(cpf: str) -> ClientEntity:
        """Get a client by it's cpf"""
        client = db.session.query(ClientModel).get(cpf)
        if not client:
            raise ClientDoesNotExistError
        return ClientEntity.from_orm(client)

    @staticmethod
    def get_all_clients() -> List[ClientEntity]:
        """Get all clients"""
        clients = db.session.query(ClientModel).all()
        clients_list = [ClientEntity.from_orm(client) for client in clients]
        return clients_list
