from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from system.domain.enums.enums import PaymentStatusEnum


class PaymentEntity(BaseModel):
    id: Optional[int] = None
    qr_code: Optional[str] = None
    status_updated_at: Optional[datetime] = None
    status: PaymentStatusEnum = PaymentStatusEnum.UNPAID

    class Config:
        from_attributes = True
        use_enum_values = True
