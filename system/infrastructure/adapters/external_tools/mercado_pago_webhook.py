from datetime import datetime
from psycopg2 import IntegrityError
from system.domain.entities.payment import PaymentEntity
from system.domain.enums.enums import PaymentStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.payment_model import PaymentModel
from system.infrastructure.adapters.external_tools.exceptions.mercado_pago_exceptions import MercadoPagoError


class MercadoPagoWebhook:
    @classmethod
    def create_qr_code_payment(cls) -> str:
        """Create payment"""
        try:
            qr_code = "qr_code"
        except Exception:
            raise MercadoPagoError
        return qr_code