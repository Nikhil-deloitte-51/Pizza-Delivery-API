from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"
    delivery = "delivery"

class DeliveryStatus(str, Enum):
    delivered = "Delivered"
    out_of_delivery = "Out for Delivery"
    pending = "Pending"
    rejected = "Rejected"

class OrderStatus(str, Enum):
    cancelled = "Cancelled"
    preparing = "Food is Preparing"
    delivered = "Delivered"
