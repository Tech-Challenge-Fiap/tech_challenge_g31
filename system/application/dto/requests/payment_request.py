from pydantic import BaseModel

from system.domain.enums.enums import PaymentStatusEnum


class PaymentRequest(BaseModel):
    status: PaymentStatusEnum = PaymentStatusEnum.UNPAID

    class Config:
        from_attributes = True
