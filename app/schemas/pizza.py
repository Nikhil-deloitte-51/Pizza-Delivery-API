from pydantic import BaseModel

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    type: str

class Pizza(PizzaBase):
    id: int

    class Config:
        orm_mode = True

class PizzaCreate(PizzaBase):
    pass