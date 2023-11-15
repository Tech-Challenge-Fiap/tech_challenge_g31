from app import app
from flask import request
from pydantic import ValidationError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.payment_exceptions import PaymentDoesNotExistsError
from system.application.usecase import payment_usecase


@app.route("/webhook/update_payment", methods=["POST"])
def update_payment():
    try:
        request_json = request.get_json()
    except ValidationError as ex:
        return ex.errors(), 400

    type = request_json.get("type")
    action = request_json.get("action")
    if action == "payment.updated" and type == "payment":
        try:
            payment_usecase.UpdatePayment.execute(request_json)
        except InfrastructureError:
            return {"error": "Internal Error"}, 500
        except PaymentDoesNotExistsError:
            return {}, 200
    return {}, 200
