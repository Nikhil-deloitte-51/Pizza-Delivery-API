from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.order import Order
from models.user import User

from enums import OrderStatus, UserRole
from database import get_db
from dependencies import get_current_user, role_required

router = APIRouter()

@router.get("/")
def get_previous_order(user_id: int, 
                       db: Session = Depends(get_db)
                       ):
    order = db.query(Order).filter(
        Order.user_id == user_id
        ).all()
    
    if not order:
        raise HTTPException(
            status_code= 404, 
            detail= "Order not found")
    return order

@router.put("/update/{order_id}",
            dependencies=[Depends(role_required(UserRole.admin))]
            )
def update_order(order_id: int, 
                 order_status: OrderStatus,
                 current_user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    
    # Fetch the order by ID 
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    # Check if order already exists
    if not order:
        raise HTTPException(
            status_code = 404,
            detail = "Order not found"
        )
    
    # Update the order details
    order.status = order_status

    # Commit the changes to the database
    db.commit()
    db.refresh(order)

    return{
        "message": "Order updated successfully",
        "order": order
    }
