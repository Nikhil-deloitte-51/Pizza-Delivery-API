from fastapi import FastAPI

from database import engine, Base
from routers import cart, admin, customer, delivery, user
from models import User, Pizza, Order, Delivery, Cart

try:
    Base.metadata.create_all(bind=engine)
    print("tables created")
except Exception as e:
    print(f"error creating tables:{e}")

app = FastAPI(
    title="Pizza Delivery API",
    description="API for managing pizza orders, users, and deliveries"
)

app.include_router(user.router, prefix="/user", tags = ["User"])
app.include_router(cart.router, prefix="/cart", tags = ["Cart"])
app.include_router(admin.router, prefix="/admin", tags = ["Admin"])
app.include_router(customer.router, prefix="/customer", tags = ["Customer"])
app.include_router(delivery.router, prefix="/delivery", tags = ["Delivery"])

@app.get("/")
def get():
    return "hello world"