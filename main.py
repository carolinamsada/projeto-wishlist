from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine
from app import models, schemas

# Cria as tabelas no banco ao iniciar a aplicação
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="✨ Glam Wishlist API",
    description="Sua lista de desejos mais cute do mundo 🛍️💖",
    version="1.0.0",
)


@app.get("/")
def root():
    """Endpoint de health check — confirma que a API está no ar."""
    return {"message": "✨ Glam Wishlist is live! Time to shop 🛍️"}


@app.post("/items", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Adiciona um novo item à wishlist."""
    db_item = models.WishlistItem(
        name=item.name,
        brand=item.brand,
        price=item.price,
        category=item.category,
        link=item.link,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items", response_model=List[schemas.ItemResponse])
def list_items(db: Session = Depends(get_db)):
    """Retorna todos os itens da wishlist."""
    return db.query(models.WishlistItem).all()


@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Busca um item específico pelo ID."""
    item = db.query(models.WishlistItem).filter(models.WishlistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found 💔")
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Remove um item da wishlist pelo ID."""
    item = db.query(models.WishlistItem).filter(models.WishlistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found 💔")
    db.delete(item)
    db.commit()
