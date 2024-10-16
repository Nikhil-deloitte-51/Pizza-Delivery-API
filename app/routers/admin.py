from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import schemas, models
from database import get_db
from dependencies import role_required
from enums import UserRole
from routers.user import get_current_user

router = APIRouter()

@router.post("/pizzas", 
             response_model= schemas.Pizza, 
             dependencies=[Depends(role_required(UserRole.admin))]
             )
def create_pizza(pizza: schemas.PizzaCreate, 
                 current_user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    """Create a new pizza record in the database"""

    # Create a new pizza instance using the provided schema data
    db_pizza = models.Pizza(**pizza.dict())
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza

@router.put("/pizzas/{pizza_id}", 
            response_model= schemas.Pizza, 
            dependencies=[Depends(role_required(UserRole.admin))]
            )
def update_pizza(pizza_id: int, pizza: schemas.PizzaCreate, 
                 current_user: models.User = Depends(get_current_user),
                 db:Session = Depends(get_db)
                 ):
    """Update an existing pizza record by its ID."""

    # Find the pizza record by its ID
    db_pizza = db.query(models.Pizza).filter(
        models.Pizza.id == pizza_id
        ).first()
    
    if not db_pizza:
        # Raise an error if the pizza record does not exist
        raise HTTPException(
            status_code= 404, 
            detail="Pizza not found",
            )
    # Update the pizza attributes with the provided data
    for key, value in pizza.dict().items():
        setattr(db_pizza, key, value)       # Set each attributes to the new value

    db.commit()
    return db_pizza

@router.delete("/pizza/{pizza_id}",
               dependencies=[Depends(role_required(UserRole.admin))]
               )
def delete_pizza(pizza_id: int, 
                 current_user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    """Delete a pizza record by its ID."""

    # Find the pizza record by its ID
    db_pizza = db.query(models.Pizza).filter(
        models.Pizza.id == pizza_id
        ).first()
    
    if not db_pizza:
        # Raise an error if the pizza record does not exist
        raise HTTPException(
            status_code=404, 
            detail= "Pizza not found",
            )

    db.delete(db_pizza)
    db.commit()
    return {
        "detail":"Pizza deleted"
        }
