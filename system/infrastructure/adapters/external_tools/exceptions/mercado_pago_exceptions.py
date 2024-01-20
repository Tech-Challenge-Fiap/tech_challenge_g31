from system.application.exceptions.payment_service_exceptions import PaymentServiceException


class MercadoPagoError(PaymentServiceException):
    def __init__(self, msg: str = "Mercado Pago Error", *args: object):  # noqa: WPS612
        super().__init__(msg, *args)