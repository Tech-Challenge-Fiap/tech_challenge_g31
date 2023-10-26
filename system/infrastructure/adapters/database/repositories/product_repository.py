from typing import Any, Dict, List
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from system.domain.entities.product import ProductEntity
from system.infrastructure.adapters.database.exceptions.product_exceptions import (
    ProductDeleteError,
    ProductDoesNotExistError,
    ProductUpdateError,
)
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.product_model import ProductModel


class ProductRepository:
    @staticmethod
    def create_product(product: ProductEntity) -> ProductEntity:
        """Create product"""
        product_to_insert = ProductModel(**product.model_dump())
        db.session.add(product_to_insert)
        db.session.commit()
        inserted_product = (
            db.session.query(ProductModel).filter_by(name=product.name).first()
        )
        return ProductEntity(**inserted_product.__dict__)

    @staticmethod
    def get_product_by_id(product_id: int) -> ProductEntity:
        """Get a product by it's id"""
        product = (
            db.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        if not product:
            raise ProductDoesNotExistError
        return ProductEntity.from_orm(product)

    @staticmethod
    def get_products_by_ids(product_ids: List[int]) -> ProductEntity:
        """Get a product by it's id"""
        products = (
            db.session.query(ProductModel)
            .filter(ProductModel.product_id.in_(product_ids))
            .all()
        )
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @staticmethod
    def get_products_by_type(produc_type: int) -> List[ProductEntity]:
        """Get products by type"""
        products = db.session.query(ProductModel).filter_by(type=produc_type).all()
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @staticmethod
    def get_all_products() -> List[ProductEntity]:
        """Get all products"""
        products = db.session.query(ProductModel).all()
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @staticmethod
    def delete_product_by_id(product_id: int) -> bool:
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

    @staticmethod
    def update_product(product_id: int, request: Dict[str, Any]) -> ProductEntity:
        """Update product"""
        product = (
            db.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        if not product:
            raise ProductDoesNotExistError
        update_attributes = {
            "type": request.type,
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
