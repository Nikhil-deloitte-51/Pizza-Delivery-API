from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.models import Pizza
from app.database import get_db

router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.post("/", response_model=Pizza, status_code= status.HTTP_201_CREATED)
async def add_pizza(pizza:Pizza, db:Session = Depends(get_db)):
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    return pizza

@router.put("{pizza_id}", response_model=Pizza, status_code=status.HTTP_200_OK)
async def update_pizza(pizza_id: int, pizza: Pizza, db: Session = Depends(get_db)):
    db_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found")
    
    for key, value in pizza.dict().items:
        setattr(db_pizza, key, value)

@router.delete("/{pizza_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_pizza(pizza_id:int, db:Session= Depends(get_db)):
    if not db_pizza:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found")

    db.delete(db_pizza)
    db.commit()
    return