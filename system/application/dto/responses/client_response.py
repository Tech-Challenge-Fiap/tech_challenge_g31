from typing import List
from flask import Response

class ClientResponse(Response):
    cpf: str
    name: str
    email: str

    class Config:
        from_attributes = True

class CreateClientResponse(ClientResponse):
    pass

class GetClientByCPFResponse(ClientResponse):
    pass

class GetAllClientsResponse(ClientResponse):
    clients: List[ClientResponse]