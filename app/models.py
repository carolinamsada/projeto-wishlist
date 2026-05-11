from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class WishlistItem(Base):
    """Representa um item salvo na wishlist."""

    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)        # Nome do produto
    brand = Column(String, nullable=True)         # Marca (opcional)
    price = Column(Float, nullable=True)          # Preço estimado (opcional)
    category = Column(String, nullable=True)      # Ex: "makeup", "skincare", "fashion"
    link = Column(String, nullable=True)          # Link para compra (opcional)
