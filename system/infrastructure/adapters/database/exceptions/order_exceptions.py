class OrderAlreadyExistsError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Order already exists",
        *args: object,
    ):
        super().__init__(msg, *args)


class OrderDoesNotExistError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Order does not exist",
        *args: object,
    ):
        super().__init__(msg, *args)


class OrderUpdateError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Order could not be updated",
        *args: object,
    ):
        super().__init__(msg, *args)
