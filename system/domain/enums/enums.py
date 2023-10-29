from enum import Enum

class OrderStatusEnum(str, Enum):
    CANCELED = "CANCELED"
    TO_BE_PAYED = "WAITING PAYMENT"
    RECIEVED = "RECIEVED"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"


class ProductTypeEnum(str, Enum):
    SNACK = "SNACK"
    SIDE = "SIDE"
    BEVERAGE = "BEVERAGE"
    DESSERT = "DESSERT"


class PaymentStatusEnum(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
