from abc import ABC, abstractmethod
from typing import Any
from flask import Response

from pydantic import BaseModel

class UseCase(ABC):
    @abstractmethod
    def execute(self, request: BaseModel) -> Response:
        raise NotImplementedError()


class UseCaseNoResponse(ABC):
    @abstractmethod
    def execute(self, request: BaseModel) -> None:
        raise NotImplementedError()


class UseCaseNoRequest(ABC):
    @abstractmethod
    def execute(self, request: BaseModel) -> Response:
        raise NotImplementedError()