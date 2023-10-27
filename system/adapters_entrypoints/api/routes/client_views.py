from app import app
from flask import request
from pydantic import ValidationError
from system.application.usecase import client_usecase
from system.application.dto.requests.client_request import CreateClientRequest
from system.infrastructure.adapters.database.exceptions.client_exceptions import (
    ClientAlreadyExistsError,
    ClientDoesNotExistError,
)

@app.route("/create_client", methods=["POST"])
def create_client():
    try:
        create_client_request = CreateClientRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        client = client_usecase.CreateClientUseCase.execute(request=create_client_request)
    except ClientAlreadyExistsError:
        return {"error": "This Client already exists"}, 409
    except Exception:
        return {"error": "Internal Error"}, 500
    return client.response


@app.route("/get_client/<cpf>", methods=["GET"])
def get_client_by_cpf(cpf):
    try:
        client = client_usecase.GetClientByCPFUseCase.execute(cpf=cpf)
    except ClientDoesNotExistError:
        return {"error": "This Client does not exist"}, 404
    except Exception:
        return {"error": "Internal Error"}, 500
    return client.response


@app.route("/get_clients/", methods=["GET"])
def get_clients():
    try:
        clients = client_usecase.GetAllClientsUseCase.execute()
        clients_list = [vars(client) for client in clients.response]
    except Exception:
        return {"error": "Internal Error"}, 500
    return clients_list
