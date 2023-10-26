from enum import Enum


class OrderStatusEnum(Enum):
    RECIEVED = "RECIEVED"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"


class ProductTypeEnum(Enum):
    SNACK = "SNACK"
    SIDE = "SIDE"
    BEVERAGE = "BEVERAGE"
    DESSERT = "DESSERT"


class PaymentStatusEnum(Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
