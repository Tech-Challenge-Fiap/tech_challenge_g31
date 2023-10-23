from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from system.domain.enums.enums import PaymentStatusEnum


class PaymentEntity(BaseModel):
    payment_id: Optional[int]
    qr_code: str
    payed_at: datetime = datetime.now()
    status: PaymentStatusEnum = PaymentStatusEnum.UNPAID

    class Config:
        from_attributes = True