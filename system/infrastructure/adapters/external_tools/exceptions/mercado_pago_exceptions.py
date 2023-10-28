class MercadoPagoError(Exception):
    def __init__(self, msg: str = "Mercado Pago Error", *args: object):  # noqa: WPS612
        super().__init__(msg, *args)