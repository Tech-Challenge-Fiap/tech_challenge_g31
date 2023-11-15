class PaymentDoesNotExistsError(Exception):
    def __init__(
        self,
        msg: str = "This Payment does not exist",
        *args: object,
    ):
        super().__init__(msg, *args)
