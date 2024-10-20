from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from models.cart import Cart
from models.order import Order
from models.user import User
from models.delivery import Delivery
from routers.payment import simulate_payment_gateway
import requests, uuid

from schemas import cart
from database import get_db, SessionLocal
from dependencies import role_required
from enums import UserRole
from dependencies import get_current_user

router = APIRouter()

@router.post("", response_model= cart.Cart, 
             dependencies=[Depends(role_required(UserRole.customer))],
             status_code= status.HTTP_201_CREATED
             )
def add_to_cart(cart_request: cart.CartCreate, 
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    """ Add an item to the cart or update the quantity if it already exists"""

    cart = db.query(Cart).filter(
        and_(
            Cart.user_id == current_user.id, 
            Cart.pizza_id == cart_request.pizza_id)
            ).first()
    cart_item = {
        "user_id": current_user.id,
        "pizza_id": cart_request.pizza_id,
        "quantity": cart_request.quantity,
        "total": cart_request.total
    }
    if not cart:
        cart = Cart(**cart_item)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if the item already exists in the user's cart
    existing_item = db.query(Cart).filter(
        Cart.user_id == cart.user_id,
        Cart.pizza_id == cart.pizza_id,
    ).first()

    if existing_item:
        # If the item exists, increase the quantity
        existing_item.quantity+= cart_request.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    return cart

@router.delete("/{cart_id}",
               dependencies=[Depends(role_required(UserRole.customer))]
               )
def remove_from_cart(cart_id: int,
                     current_user: User = Depends(get_current_user), 
                     db: Session = Depends(get_db)
                     ):
    """Remove an item from the cart by its ID."""

    # Find the cart item by its ID
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id
        ).first()
    
    if not cart_item:
        # Raise an error if the item does not exist
        raise HTTPException(
            status_code=404, 
            detail= "Cart item not found",
            )
    
    # Delete the cart item from the session
    db.delete(cart_item)
    db.commit()
    return {"detail": "Item removed from cart"}

@router.get("/{user_id}",
            dependencies=[Depends(role_required(UserRole.customer))]
            )
def get_cart(user_id: int, 
             current_user: User = Depends(get_current_user),
             db: Session = Depends(get_db)
             ):
    """Retrieve all items in the cart for a specific user."""

    # Query to get all cart items for the given user ID
    Items = db.query(Cart).filter(
        Cart.user_id == user_id
        ).all()
    
    if not Items:
        raise HTTPException(
            status_code=400, 
            detail= "Cart is empty"
            )
    
    return {
        "user_id": user_id, "Items": Items
        }

def send_order_to_delivery_partner(
        user_id: int, 
        order_number: str, 
        delivery_address: str
        ):
    
    # Delivery partner url
    delivery_api_url = "http://127.0.0.1:8000/delivery/deliveries"
    
    # Creating a payload for Delivery Partner API
    payload = {
        "user_id": user_id,
        "order_number": order_number,
        "delivery_address": delivery_address
    }

    response = requests.post(
        delivery_api_url,
        json=payload
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code = response.status_code,
            detail = response.text
        )

@router.post("/checkout")
def checkout(user_id: int, 
             db:Session = Depends(get_db)
             ):
    
    # Check for user_id present in cart
    cart_items = db.query(Cart).filter(
        Cart.user_id == user_id
        ).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=400, 
            detail= "Cart is empty"
            )
    
    # Adding the total value of item present in cart
    total_amount = sum(item.quantity * item.total for item in cart_items)

    db = SessionLocal()

    # TODO Mocking the online method
    payment_method = "Online"

    # TODO Mocking successful response
    payment_response = simulate_payment_gateway(db,user_id, payment_method, total_amount)

    if payment_response["status"] != "success":
        db.close()
        raise HTTPException(
            status_code = 400,
            detail = "Payment processing failed"
        )
    
    # Generating a unique order number
    order_number = str(uuid.uuid4())

    # Creating a new order for user
    new_order = Order(user_id = user_id,
                     description = "Your pizza order is confirmed",
                     order_number = order_number,
                     status = "Successflly placed",
                     instruction = "No olives"
                    )
        
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # TODO Mocking the delivery_address
    delivery_address = "flat.No. 2105, London, Uk"

    # Send the order to the delivery partner 
    send_order_to_delivery_partner(user_id, order_number, delivery_address)

    db.query(Cart).filter(
        Cart.user_id==user_id
        ).delete()
    
    db.commit()

    db.close()

    return{
        "order_number": order_number,
        "status": "Checkout completed successfully",
        # "delivery_id": delivery.id,
        "payment_message": payment_response["message"]
    }