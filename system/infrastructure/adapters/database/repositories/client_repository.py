from typing import List
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from system.application.exceptions.client_exceptions import ClientAlreadyExistsError
from system.application.ports.client_port import ClientPort
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.client_model import ClientModel


class ClientRepository(ClientPort):
    @classmethod
    def create_client(cls, client: ClientEntity) -> ClientEntity:
        """Create client"""
        client_to_insert = ClientModel(**client.model_dump())
        try:
            db.session.add(client_to_insert)
            db.session.commit()
            db.session.flush()
        except IntegrityError as error:
            if isinstance(error.orig, UniqueViolation):
                raise ClientAlreadyExistsError
            raise PostgreSQLError("PostgreSQL Error")
        return ClientEntity.from_orm(client_to_insert)

    @classmethod
    def get_client_by_cpf(cls, cpf: str) -> ClientEntity:
        """Get a client by it's cpf"""
        try:
            client = db.session.query(ClientModel).get(cpf)
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not client:
            raise NoObjectFoundError
        return ClientEntity.from_orm(client)

    @classmethod
    def get_all_clients(cls) -> List[ClientEntity]:
        """Get all clients"""
        try:
           clients = db.session.query(ClientModel).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        clients_list = [ClientEntity.from_orm(client) for client in clients]
        return clients_list
