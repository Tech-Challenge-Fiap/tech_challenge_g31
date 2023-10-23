from pydantic import BaseModel

class ClientEntity(BaseModel):
    cpf: str
    name: str
    email: str

    class Config:
        from_attributes = True