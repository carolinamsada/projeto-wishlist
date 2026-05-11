import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Em testes, usa banco em memória; em produção, usa arquivo SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wishlist.db")

# connect_args necessário apenas para SQLite (permite uso em múltiplas threads)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency que fornece uma sessão de banco para cada request e fecha ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
