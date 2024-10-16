from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"
    delivery = "delivery"