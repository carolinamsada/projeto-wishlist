from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    """Schema de entrada para criação de um item."""
    name: str
    brand: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    link: Optional[str] = None


class ItemResponse(BaseModel):
    """Schema de saída — inclui o ID gerado pelo banco."""
    id: int
    name: str
    brand: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    link: Optional[str] = None

    class Config:
        # Permite que o Pydantic leia atributos de objetos SQLAlchemy diretamente
        from_attributes = True
