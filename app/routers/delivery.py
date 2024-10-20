from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from models.delivery import Delivery
from models.user import User

from schemas.delivery import DeliveryCreate, DeliveryRequest, DeliveryStatusUpdate
from database import get_db

from dependencies import role_required
from enums import UserRole, DeliveryStatus
from dependencies import get_current_user

router = APIRouter()

@router.patch("/deliveries/{delivery_id}/status",
              dependencies=[Depends(role_required(UserRole.delivery))]
              )
def update_delivery_status(delivery_id: int, delivery_status: DeliveryStatus,
                           comment: str = None, 
                           current_user: User = Depends(get_current_user),
                           db: Session = Depends(get_db)
                           ):
    """Update the status of an existing delivery record."""
    
    # Find the delivery record by its ID
    delivery = db.query(Delivery).filter(
        Delivery.id == delivery_id
        ).first()
    
    if not delivery:
        # Raise an error if the delivery record does not exist
        raise HTTPException(
            status_code=404, 
            detail= "Delivery not found",
            )

    # Update the delivery status with the new status
    delivery.delivery_status = delivery_status

    if comment: # If a comment is provided, update the delivery comment
        delivery.comment = comment

    # Set the start time when the delivery status changes to "in_progress"
    if delivery_status == "Out for Delivery" and not delivery.start_time:
        delivery.start_time = datetime.now().isoformat()

    # Set the end time when the delivery status changes to "delivered"
    elif delivery_status == "Delivered":
        delivery.end_time = datetime.now().isoformat()

    db.commit()         # Commit the changes to the database
    return {
        "detail": "Delivery status updated", 
        "comment": delivery.comment, 
        "start_time": delivery.start_time, 
        "end_time": delivery.end_time
        }


@router.post("/deliveries"
             )
def create_delivery(delivery_request: DeliveryRequest, 
                    db: Session = Depends(get_db)
                    ):
    """Create a new delivery record in the database."""
    
    existing_delivery = db.query(Delivery).filter(
        Delivery.order_number == delivery_request.order_number
        ).first()
    
    if existing_delivery:
        db.close()
        raise HTTPException(
            status_code = 404,
            detail = "Delivery order already exists"
        )
    
    delivery = Delivery(
        user_id = delivery_request.user_id,
        order_number = delivery_request.order_number,
        delivery_address = delivery_request.delivery_address,
        delivery_status = "Pending"
    )
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    db.close()

    return {
            "delivery_id": delivery.id,
            "message": "Delivery order created"
            }
    