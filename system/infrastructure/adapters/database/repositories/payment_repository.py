from system.domain.entities.payment import PaymentEntity
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.payment_model import PaymentModel


class PaymentRepository:
    @classmethod
    def create_payment(cls, payment: PaymentEntity) -> PaymentEntity:
        """Create payment"""
        payment_to_insert = PaymentModel(**payment.model_dump())
        db.session.add(payment_to_insert)
        db.session.commit()
        return PaymentEntity.from_orm(payment_to_insert)
