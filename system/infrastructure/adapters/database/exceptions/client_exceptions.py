class ClientAlreadyExistsError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Client already exists",
        *args: object,
    ):
        super().__init__(msg, *args)

class ClientDoesNotExistError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Client does not exist",
        *args: object,
    ):
        super().__init__(msg, *args)