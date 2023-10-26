class ProductAlreadyExistsError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Product already exists",
        *args: object,
    ):
        super().__init__(msg, *args)


class ProductDoesNotExistError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Product does not exist",
        *args: object,
    ):
        super().__init__(msg, *args)


class ProductUpdateError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Product could not be updated",
        *args: object,
    ):
        super().__init__(msg, *args)


class ProductDeleteError(Exception):
    def __init__(  # noqa: WPS612
        self,
        msg: str = "This Product could not be deleted",
        *args: object,
    ):
        super().__init__(msg, *args)
