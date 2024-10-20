from fastapi import FastAPI

from database import engine, Base
from routers import cart, delivery, user, orders, pizzas, payment


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
app.include_router(orders.router, prefix="/order", tags = ["Order"])
app.include_router(pizzas.router, prefix="/pizza", tags = ["PIzza"])
app.include_router(delivery.router, prefix="/delivery", tags = ["Delivery"])
app.include_router(payment.router, prefix="/payment", tags = ["Payment"])

@app.get("/")
def get():
    return "hello world"