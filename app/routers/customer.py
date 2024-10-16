from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import schemas, models
from database import get_db
from dependencies import role_required
from enums import UserRole
from routers.user import get_current_user

router = APIRouter()

@router.get("/pizzas", 
            response_model=list[schemas.Pizza], 
            dependencies=[Depends(role_required(UserRole.customer))]
            )
def get_pizzas(current_user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)
               ):
    return db.query(models.Pizza).all()

@router.post("/", 
             response_model= schemas.Order, 
             dependencies=[Depends(role_required(UserRole.customer))],
             status_code=status.HTTP_201_CREATED
             )
async def create_order(order: schemas.OrderCreate, 
                       current_user: models.User = Depends(get_current_user),
                       db: Session =Depends(get_db)
                       ):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/{user_id}", 
            response_model= list[schemas.Order],
            dependencies=[Depends(role_required(UserRole.customer))]
            )
def get_previous_orders(user_id: int, 
                        current_user: models.User = Depends(get_current_user),
                        db: Session = Depends(get_db)
                        ):
    
    orders = db.query(models.Order).filter(
        models.Order.user_id == user_id
        ).all()
    
    if not orders:
        raise HTTPException(
            status_code=404, 
            detail= "No orders found for this user",
            )
    
    return orders

