from app import app
from flask import request
from pydantic import ValidationError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.payment_exceptions import PaymentDoesNotExistsError
from system.application.ports.payment_service_port import PaymentService
from system.application.usecase import payment_usecase
from system.infrastructure.adapters.database.repositories.payment_repository import PaymentRepository
from system.infrastructure.adapters.external_tools.mercado_pago import MercadoPago


@app.route("/webhook/update_payment", methods=["POST"])
def update_payment():
    try:
        request_json = request.get_json()
    except ValidationError as ex:
        return ex.errors(), 400
    payment_client: PaymentService = MercadoPago
    type = request_json.get("type")
    action = request_json.get("action")

    if action == "payment.updated" and type == "payment":
        try:
            payment_usecase.UpdatePayment.execute(request_json, payment_service=MercadoPago(), payment_repository=PaymentRepository)
        except InfrastructureError:
            return {"error": "Internal Error"}, 500
        except PaymentDoesNotExistsError:
            return {}, 200
    return {}, 200
