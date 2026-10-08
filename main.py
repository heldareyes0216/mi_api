import uvicorn
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select

from database import init_db, get_session
from models import User, UserCreate, UserUpdate, Product, ProductCreate, ProductUpdate

app = FastAPI(title="API CRUD con Supabase & SQLModel")


# RUTAS DE USUARIOS
@app.get("/users", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    db_user = User.model_validate(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_dict = user_data.model_dump(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(db_user, key, value)
        
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    session.delete(db_user)
    session.commit()
    return {"message": "Usuario eliminado correctamente"}


# RUTAS DE PRODUCTOS
@app.get("/products", response_model=List[Product])
def get_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    limit: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = select(Product)

    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))
    if category:
        query = query.where(Product.category.ilike(category))
    if limit:
        query = query.limit(limit)

    return session.exec(query).all()

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: ProductUpdate, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product_dict = product_data.model_dump(exclude_unset=True)
    for key, value in product_dict.items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    session.delete(db_product)
    session.commit()
    return {"message": "Producto eliminado correctamente"}


def start():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)