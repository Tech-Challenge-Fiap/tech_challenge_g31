from typing import Any, Dict, List
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2.errors import UniqueViolation
from system.application.exceptions.product_exceptions import ProductAlreadyExistsError, ProductUpdateError
from system.application.ports.product_port import ProductPort
from system.domain.entities.product import ProductEntity
from system.application.exceptions.repository_exceptions import InvalidInputError, NoObjectFoundError
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import PostgreSQLError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.product_model import ProductModel


class ProductRepository(ProductPort):
    @classmethod
    def create_product(cls, product: ProductEntity) -> ProductEntity:
        """Create product"""
        product_to_insert = ProductModel(**product.model_dump())
        db.session.add(product_to_insert)
        try:
            db.session.commit()
            db.session.flush()
        except IntegrityError as error:
            if isinstance(error.orig, UniqueViolation):
                raise ProductAlreadyExistsError
            raise PostgreSQLError
        return ProductEntity.from_orm(product_to_insert)

    @classmethod
    def get_product_by_id(cls, product_id: int) -> ProductEntity:
        """Get a product by it's id"""
        try:
            product = (
                db.session.query(ProductModel).filter_by(product_id=product_id, is_active = True).first()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not product:
            raise NoObjectFoundError
        return ProductEntity.from_orm(product)

    @classmethod
    def get_products_by_ids(cls, product_ids: List[int]) -> ProductEntity:
        """Get a product by it's id"""
        try:
            products = (
                db.session.query(ProductModel)
                .filter(ProductModel.product_id.in_(product_ids))
                .filter(ProductModel.is_active == True)
                .all()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not products:
            raise NoObjectFoundError
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @classmethod
    def get_products_by_type(cls, produc_type: int) -> List[ProductEntity]:
        """Get products by type"""
        try:
            products = db.session.query(ProductModel).filter_by(type=produc_type,  is_active = True).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        except DataError:
            raise InvalidInputError
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @classmethod
    def get_all_products(cls) -> List[ProductEntity]:
        """Get all products"""
        try:
            products = db.session.query(ProductModel).filter_by(is_active = True).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list

    @classmethod
    def delete_product_by_id(cls, product_id: int) -> None:
        """Delete product by its id"""
        try:
            product = (
                db.session.query(ProductModel).filter_by(product_id=product_id, is_active = True).first()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not product:
            raise NoObjectFoundError
        product.is_active = False
        try:
            db.session.commit()
        except IntegrityError as ex:
            raise PostgreSQLError("PostgreSQL Error")

    @classmethod
    def update_product(cls, product_id: int, request: Dict[str, Any]) -> ProductEntity:
        """Update product"""
        try:
            product = (
                db.session.query(ProductModel).filter_by(product_id=product_id, is_active = True).first()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not product:
            raise NoObjectFoundError
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
        except Exception:
            raise ProductUpdateError
        return ProductEntity.from_orm(product)
    
    @classmethod
    def enable_product_by_id(cls, product_id: int) -> ProductEntity:
        """Enable product by its id"""
        try:
            product = (
                db.session.query(ProductModel).filter_by(product_id=product_id).first()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not product:
            raise NoObjectFoundError
        product.is_active = True
        try:
            db.session.commit()
        except IntegrityError as ex:
            raise PostgreSQLError("PostgreSQL Error")
        return ProductEntity.from_orm(product)
    
    @classmethod
    def get_deleted_products(cls) -> List[ProductEntity]:
        """Get all products"""
        try:
            products = db.session.query(ProductModel).filter_by(is_active = False).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        products_list = [ProductEntity.from_orm(product) for product in products]
        return products_list
