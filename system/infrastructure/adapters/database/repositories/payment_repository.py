from datetime import datetime
from psycopg2 import IntegrityError
from system.domain.entities.payment import PaymentEntity
from system.domain.enums.enums import PaymentStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import PostgreSQLError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.payment_model import PaymentModel
from system.infrastructure.adapters.external_tools.mercado_pago_webhook import MercadoPagoWebhook
from system.infrastructure.adapters.external_tools.exceptions.mercado_pago_exceptions import MercadoPagoError


class PaymentRepository:
    @classmethod
    def create_payment(cls) -> PaymentEntity:
        """Create payment"""
        try:
            qr_code = MercadoPagoWebhook.create_qr_code_payment()
        except Exception:
            raise MercadoPagoError
        payment = PaymentEntity(qr_code=qr_code)
        payment_to_insert = PaymentModel(**payment.model_dump())
        try:
            db.session.add(payment_to_insert)
            db.session.commit()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error") 
        return PaymentEntity.from_orm(payment_to_insert)

    @classmethod
    def update_payment(cls, payment_id: int, payment_status: PaymentStatusEnum) -> PaymentEntity:
        """update payment by its id"""
        try:
            payment = (
                db.session.query(PaymentModel).filter_by(id=payment_id).first()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not payment:
            payment = PaymentRepository.create_payment()
        payment.status = payment_status
        payment.payed_at = datetime.now()
        try:
            db.session.commit()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        return PaymentEntity.from_orm(payment)
