from typing import Optional 
from sqlmodel import SQLModel, Field

# creamos la tbalas y esquemas para los usuarios 
class User(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str

class UserCreate(SQLModel):
    name:str

class UserUpdate(SQLModel):
    name:Optional[str] = None


# creamos la tabla y esquemas para los productos
class Product(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str
    price:float
    quantity:int
    category:str

class ProductCreate(SQLModel):
    name:str
    price:float
    quantity:int
    category:str

class ProductUpdate(SQLModel):
    name:Optional[str] = None
    price:Optional[float] = None
    quantity:Optional[int] = None
    category:Optional[str] = None