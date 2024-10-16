from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import OrderDB, OrderCreate, OrderResponse
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrderCreate, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: Session =Depends(get_db)):
    db_order = OrderDB(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order