from abc import abstractmethod


class PaymentServicePort:
    @classmethod
    @abstractmethod
    def create_qr_code_pix_payment(cls, payment_id) -> str:
        """
        Create payment
        """

    @classmethod
    @abstractmethod
    def get_payment_by_id(cls, payment_id) -> dict:
        """
        Get payment info
        """
