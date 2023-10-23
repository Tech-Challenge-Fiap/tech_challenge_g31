from pydantic import BaseModel

class ClientPayload(BaseModel):
    cpf: str
    name: str
    email: str

    class Config:
        from_attributes = True

class CreateClientRequest(ClientPayload):
    pass