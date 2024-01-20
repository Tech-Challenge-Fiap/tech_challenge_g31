from abc import abstractmethod
from system.domain.entities.payment import PaymentEntity
from system.domain.enums.enums import PaymentStatusEnum


class PaymentPort:
    @classmethod
    @abstractmethod
    def create_payment(cls) -> PaymentEntity:
        """Create payment"""

    @classmethod
    @abstractmethod
    def update_payment_status(
        cls, payment_id: int, payment_status: PaymentStatusEnum
    ) -> PaymentEntity:
        """update payment by its id"""
    
    @classmethod
    @abstractmethod
    def update_payment_qrcode(
        cls, payment_id: int, payment_status: PaymentStatusEnum
    ) -> PaymentEntity:
        """update payment by its id"""

    @classmethod
    @abstractmethod
    def get_payment_from_order(cls, order_id) -> PaymentEntity:
        """get payment by order identifier"""

    @classmethod
    @abstractmethod
    def get_payment_by_id(cls, payment_id) -> PaymentEntity:
        """get payment by its id"""
