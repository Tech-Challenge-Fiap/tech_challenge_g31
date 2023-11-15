from flask_restful import Resource
from system.application.dto.responses.order_response import (
    CheckOrderPaymentResponse,
)
from system.application.exceptions.order_exceptions import (
    OrderDoesNotExistError,
)
from system.application.exceptions.payment_exceptions import PaymentDoesNotExistsError
from system.application.usecase.usecases import UseCase
from system.domain.enums.enums import OrderStatusEnum, PaymentStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    NoObjectFoundError,
)
from system.infrastructure.adapters.database.repositories.payment_repository import (
    PaymentRepository,
)
from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)
from system.infrastructure.adapters.external_tools.mercado_pago import MercadoPago


class UpdateOrderPaymentUseCase(UseCase, Resource):
    def execute(order_id: int) -> CheckOrderPaymentResponse:
        """
        Get order's payment status
        """
        try:
            order = OrderRepository.get_order_by_id(order_id=order_id)
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        if (
            order.payment.status == PaymentStatusEnum.PAID
            and order.status == OrderStatusEnum.TO_BE_PAYED
        ):
            OrderRepository.update_order_status(
                order_id, status=OrderStatusEnum.RECIEVED
            )
        return CheckOrderPaymentResponse(order.payment.model_dump())


class UpdatePayment(UseCase, Resource):
    def execute(request_json: dict) -> None:
        """
        Get order's payment status
        """

        payment_external_id = request_json.get("data", {}).get("id")
        if not payment_external_id:
            return
        payment_info = MercadoPago.get_payment_by_id(payment_external_id)
        try:
            payment = PaymentRepository.get_payment_by_id(
                payment_info["external_reference"]
            )
        except NoObjectFoundError:
            raise PaymentDoesNotExistsError
        if payment_info["status"] == "approved":
            PaymentRepository.update_payment_status(payment.id, PaymentStatusEnum.PAID)
        if payment_info["status"] in ("charged_back", "cancelled", "refunded"):
            PaymentRepository.update_payment_status(payment.id, PaymentStatusEnum.CANCELLED)
