from app import app
from flask import request
from psycopg2 import IntegrityError
from system.application.dto.requests.client_request import CreateClientRequest
from system.application.usecase.client_usecase import CreateClientUseCase, GetAllClientsUseCase, GetClientByCPFUseCase
from system.infrastructure.adapters.database.exceptions.client_exceptions import ClientAlreadyExistsError, ClientDoesNotExistError


@app.route('/create_client', methods=['POST'])
def create_client():
    create_client_request = CreateClientRequest(**request.get_json())
    try:
        client = CreateClientUseCase.execute(request=create_client_request)
    except ClientAlreadyExistsError:
            return "This Client already exists", 400
    return client.response

@app.route('/get_client/<cpf>', methods=['GET'])
def get_client_by_cpf(cpf):
    try:
        client = GetClientByCPFUseCase.execute(cpf=cpf)
    except ClientDoesNotExistError as err:
            return "This Client does not exist", 400
    return client.response

@app.route('/get_clients/', methods=['GET'])
def get_clients():
    try:
        clients = GetAllClientsUseCase.execute()
    except IntegrityError:
            return "Internal Error", 500
    clients_list = [vars(client) for client in clients.response]
    return clients_list
