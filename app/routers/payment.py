from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models.payment import Payment

from schemas.payment import PaymentCreate
from database import get_db, SessionLocal

router = APIRouter()

@router.get("/{payment_id}", 
            response_model = PaymentCreate
            )
def get_payment(payment_id: int, 
                db: Session = Depends(get_db)
                ):
    
    payment = db.query(Payment).filter(
        Payment.id == payment_id
        ).first()
    
    if not payment:
        raise HTTPException(
            status_code= 404, 
            detail = "Payment not found"
            )
    
    return payment

db = SessionLocal()

def simulate_payment_gateway(db,
                             user_id: int, 
                             payment_method: str, 
                             amount: float
                             ):
    
    # Save payment details
    payment_record = Payment(
        user_id=user_id,
        amount=amount,
        payment_method=payment_method,
        created_at = datetime.now().isoformat()
    )

    db.add(payment_record)
    db.commit()
    db.refresh(payment_record)

    print(f"Proccessing payment of {amount} using {payment_method}")
    
    return {
        "status": "success",
        "message": "payment processed successfully"
    }