from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from models import Order, Delivery
from database import get_db
import schemas, models
from dependencies import role_required
from enums import UserRole
from routers.user import get_current_user

router = APIRouter()

# @router.post("/deliveries", response_model=schemas.Delivery, dependencies=[Depends(role_required(UserRole.delivery))])
@router.post("/deliveries", 
             response_model=schemas.Delivery, 
             dependencies=[Depends(role_required(UserRole.delivery))]
             )
def create_delivery(delivery: schemas.DeliveryCreate, 
                    current_user: models.User = Depends(get_current_user),
                    db: Session = Depends(get_db)
                    ):
    """Create a new delivery record in the database."""

    # Create a new Delivery instance using the provided schema data
    db_delivery = models.Delivery(**delivery.dict())
    db.add(db_delivery) 
    db.commit() 
    db.refresh(db_delivery) 
    return db_delivery

@router.patch("/deliveries/{delivery_id}/status",
              dependencies=[Depends(role_required(UserRole.delivery))]
              )
def update_delivery_status(delivery_id: int, delivery_status: str, 
                           comment: str = None, 
                           current_user: models.User = Depends(get_current_user),
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
    if delivery_status == "in_progress" and not delivery.start_time:
        delivery.start_time = datetime.utcnow()

    # Set the end time when the delivery status changes to "delivered"
    elif delivery_status == "delivered":
        delivery.end_time = datetime.utcnow()

    db.commit()         # Commit the changes to the database
    return {
        "detail": "Delivery status updated", 
        "comment": delivery.comment, 
        "start_time": delivery.start_time, 
        "end_time": delivery.end_time
        }
