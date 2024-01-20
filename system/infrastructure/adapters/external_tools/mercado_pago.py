import math
import basehash
from system.application.ports.payment_service_port import PaymentService
from system.infrastructure.adapters.external_tools.exceptions.mercado_pago_exceptions import (
    MercadoPagoError,
)


b62 = basehash.base62(generator=1.7190192019129120 + math.pi)


class MercadoPago(PaymentService):
    @classmethod
    def create_qr_code_pix_payment(cls, payment_id) -> str:
        # aqui usar um md5 em cima do id do pagamento para gerar o external_reference passado de parâmetro ao mercado pago
        # external_reference = b62.hash(payment_id)
        """Create payment"""
        try:
            mocked_payment = {
                "qr_data": "00020101021243650016COM.MERCADOLIBRE02013063638f1192a-5fd1-4180-a180-8bcae3556bc35204000053039865802BR5925IZABEL AAAA DE MELO6007BARUERI62070503***63040B6D",
                "in_store_order_id": "d4e8ca59-3e1d-4c03-b1f6-580e87c654ae",
            }
        except Exception:
            raise MercadoPagoError
        return mocked_payment

    @classmethod
    def get_payment_by_id(cls, payment_id):
        """Get payment info"""
        try:
            mocked_payment = {
                "id": 1,
                "date_created": "2017-08-31T11:26:38.000Z",
                "date_approved": "2017-08-31T11:26:38.000Z",
                "date_last_updated": "2017-08-31T11:26:38.000Z",
                "money_release_date": "2017-09-14T11:26:38.000Z",
                "payment_method_id": "account_money",
                "payment_type_id": "credit_card",
                "status": "approved",
                "status_detail": "accredited",
                "currency_id": "BRL",
                "description": "Pago Pizza",
                "external_reference": "1",
                "collector_id": 2,
                "payer": {
                    "id": 123,
                    "email": "test_user_80507629@testuser.com",
                    "identification": {"type": "CPF", "number": 19119119100},
                    "type": "customer",
                },
                "metadata": {},
                "additional_info": {},
                "transaction_amount": 250,
                "transaction_amount_refunded": 0,
                "coupon_amount": 0,
                "transaction_details": {
                    "net_received_amount": 250,
                    "total_paid_amount": 250,
                    "overpaid_amount": 0,
                    "installment_amount": 250,
                },
                "installments": 1,
                "card": {},
            }
        except Exception:
            raise MercadoPagoError
        # mocked_payment["payment_id"] = b62.unhash(mocked_payment["external_reference"])
        return mocked_payment
