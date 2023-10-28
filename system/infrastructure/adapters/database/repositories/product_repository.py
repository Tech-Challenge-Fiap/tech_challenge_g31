from typing import Any, Dict, List
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from system.application.ports.product_port import ProductPort
from system.domain.entities.product import ProductEntity
from system.infrastructure.adapters.database.exceptions.product_exceptions import (
    ProductDeleteError,
    ProductDoesNotExistError,
    ProductUpdateError,
)
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.product_model import ProductModel


class ProductRepository(ProductPort):
    @classmethod
    def create_product(cls, product: ProductEntity) -> ProductEntity:
        """Create product"""
        product_to_insert = ProductModel(**product.model_dump())
        db.session.add(product_to_insert)
        db.session.commit()
        db.session.flush()
        product_to_insert.type = product_to_insert.type.value
        return ProductEntity.from_orm(product_to_insert)

    @classmethod
    def get_product_by_id(cls, product_id: int) -> ProductEntity:
        """Get a product by it's id"""
        product = (
            db.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        if not product:
            raise ProductDoesNotExistError
        return ProductEntity.from_orm(product)

    @classmethod
    def get_products_by_ids(cls, product_ids: List[int]) -> ProductEntity:
        """Get a product by it's id"""
        products = (
            db.session.query(ProductModel)
            .filter(ProductModel.product_id.in_(product_ids))
            .all()
        )
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @classmethod
    def get_products_by_type(cls, produc_type: int) -> List[ProductEntity]:
        """Get products by type"""
        products = db.session.query(ProductModel).filter_by(type=produc_type).all()
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @classmethod
    def get_all_products(cls) -> List[ProductEntity]:
        """Get all products"""
        products = db.session.query(ProductModel).all()
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @classmethod
    def delete_product_by_id(cls, product_id: int) -> bool:
        """Delete product by its id"""
        product = (
            db.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        try:
            db.session.delete(product)
            db.session.commit()
        except UnmappedInstanceError as err:
            raise ProductDoesNotExistError(str(err))
        except Exception as ex:
            raise ProductDeleteError(str(ex))
        return True

    @classmethod
    def update_product(cls, product_id: int, request: Dict[str, Any]) -> ProductEntity:
        """Update product"""
        product = (
            db.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        if not product:
            raise ProductDoesNotExistError
        update_attributes = {
            "name": request.name,
            "price": request.price,
            "prep_time": request.prep_time,
            "description": request.description,
            "image": request.image,
        }

        # Atualiza os atributos do produto com base no dicionário
        for attr, value in update_attributes.items():
            if value is not None:
                setattr(product, attr, value)
        try:
            db.session.commit()
        except IntegrityError:
            raise ProductUpdateError
        return ProductEntity.from_orm(product)
