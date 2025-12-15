from typing import Optional
from sqlmodel import Field, SQLModel

class Pizza(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ingredients: str
    price: float
