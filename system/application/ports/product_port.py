from abc import abstractmethod
from typing import List
from system.application.dto.requests.product_request import CreateProductRequest
from system.domain.enums.enums import ProductTypeEnum

from system.domain.entities.product import ProductEntity


class ProductPort:
    @classmethod
    @abstractmethod
    def create_product(payload: CreateProductRequest) -> ProductEntity:
        """
        Method that create product
        """

    @classmethod
    @abstractmethod
    def get_products_by_type(type: ProductTypeEnum) -> List[ProductEntity]:
        """
        Method that get products by type
        """

    @classmethod
    @abstractmethod
    def get_product_by_id(product_id: int) -> ProductEntity:
        """
        Method that gets a product by it's id
        """

    @classmethod
    @abstractmethod
    def get_all_products() -> List[ProductEntity]:
        """
        Method that gets all products
        """

    @classmethod
    @abstractmethod
    def update_product(product_id: int) -> ProductEntity:
        """
        Method that update product
        """

    @classmethod
    @abstractmethod
    def delete_product(product_id: int) -> ProductEntity:
        """
        Method that remove product
        """

    @classmethod
    @abstractmethod
    def get_products_by_ids(product_id: int) -> ProductEntity:
        """
        Get product by its id
        """
