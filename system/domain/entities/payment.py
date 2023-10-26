from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from system.domain.enums.enums import PaymentStatusEnum


class PaymentEntity(BaseModel):
    id: Optional[int] = None
    qr_code: str
    payed_at: Optional[datetime] = None
    status: str = PaymentStatusEnum.UNPAID.value

    class Config:
        from_attributes = True
