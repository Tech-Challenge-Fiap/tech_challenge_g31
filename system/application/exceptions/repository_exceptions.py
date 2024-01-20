class DataRepositoryExeption(Exception):
    pass


class NoObjectFoundError(DataRepositoryExeption):
    pass


class InvalidInputError(DataRepositoryExeption):
    pass
