from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from models.pizza import Pizza
from models.user import User
from schemas import pizza
from database import get_db

from dependencies import role_required, get_current_user
from enums import UserRole

router = APIRouter()

@router.post("/", 
             response_model= pizza.Pizza, 
             status_code= status.HTTP_201_CREATED,
             dependencies=[Depends(role_required(UserRole.admin))]
             )
async def add_pizza(pizza:pizza.PizzaCreate, 
                    current_user: User = Depends(get_current_user),
                    db:Session = Depends(get_db)
                    ):
    """Create a new Pizza record in database"""
   
    # Create a new pizza instance using the provided schema data
    db_pizza = Pizza(**pizza.dict())
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza

@router.put("/{pizza_id}", 
            response_model= pizza.Pizza, 
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(role_required(UserRole.admin))]
            )
async def update_pizza(pizza_id: int, 
                       pizza: pizza.Pizza, 
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)
                       ):
    """Update an existing pizza record by its ID."""

    # Find the pizza record by its ID
    db_pizza = db.query(Pizza).filter(
        Pizza.id == pizza_id
        ).first()
    
    if not pizza_id:
        # Raise an error if the pizza record does not exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pizza not found"
            )
    
    for key, value in pizza.dict().items:
        setattr(db_pizza, key, value)

    db.commit()
    db.refresh(db_pizza)
    return db_pizza

@router.delete("/{pizza_id}", 
               dependencies=[Depends(role_required(UserRole.admin))],
               status_code = status.HTTP_204_NO_CONTENT
               )
async def delete_pizza(pizza_id: int, 
                       current_user: User = Depends(get_current_user),
                       db: Session= Depends(get_db)):
    """Delete a pizza record by its ID."""

    # Find the pizza record by its ID
    db_pizza = db.query(Pizza).filter(
        Pizza.id == pizza_id
        ).first()
    
    if not db_pizza:
        # Raise an error if the pizza record does not exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pizza not found"
            )

    db.delete(db_pizza)
    db.commit()

    return {
        "detail": "Pizza deleted"
        }

@router.get("/",
            dependencies=[Depends(role_required(UserRole.admin))]
            )
def get_all_pizzas(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    
    return db.query(Pizza).all()

