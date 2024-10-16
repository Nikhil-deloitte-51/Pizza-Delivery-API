from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import Cart, CartResponse, CartItemCreate, Order, User
from database import get_db
import schemas
from dependencies import role_required
from enums import UserRole
from routers.user import get_current_user

router = APIRouter()

@router.post("", response_model= schemas.Cart, 
             dependencies=[Depends(role_required(UserRole.customer))],
             status_code= status.HTTP_201_CREATED
             )
def add_to_cart(cart: schemas.CartCreate, 
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    """ Add an item to the cart or update the quantity if it already exists"""

    # Check if the item already exists in the user's cart
    existing_item = db.query(Cart).filter(
        Cart.user_id == cart.user_id,
        Cart.pizza_id == cart.pizza_id,
    ).first()

    if existing_item:
        # If the item exists, increase the quantity
        existing_item.quantity+= cart.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Create a new cart item if it doesn't exist
    db_cart = Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

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
    
    return {
        "user_id": user_id, "Items": Items
        }

@router.post("/checkout/{user_id}",
             dependencies=[Depends(role_required(UserRole.customer))]
             )
def checkout(user_id: int, 
             current_user: User = Depends(get_current_user),
             db: Session= Depends(get_db)
             ):

    cart_items = db.query(Cart).filter(
        Cart.user_id == user_id
        ).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=400, 
            detail= "Cart is empty"
            )

    for item in cart_items:
        order = Order(
            user_id=user_id, pizza_id=item.pizza_id, status="pending"
            )
        db.add(order)

    db.query(Cart).filter(
        Cart.user_id==user_id
        ).delete()
    
    db.commit()
    return {
        "detail": "Checkout successful"
        }
