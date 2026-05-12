import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

# Banco de arquivo temporário para testes — garante que o TestClient e o fixture
# enxergam a mesma conexão (sqlite em memória tem escopo de conexão único)
TEST_DATABASE_URL = "sqlite:///./test_wishlist.db"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    """Substitui a dependency para apontar ao banco de testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Recria o schema antes de cada teste e limpa depois — garante isolamento total."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


client = TestClient(app)


# --- Teste 1: health check ---
def test_root_returns_welcome_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "live" in response.json()["message"]


# --- Teste 2: criar item com todos os campos ---
def test_create_item_full():
    payload = {
        "name": "NARS Blush Orgasm",
        "brand": "NARS",
        "price": 189.90,
        "category": "makeup",
        "link": "https://sephora.com.br/nars-blush",
    }
    response = client.post("/items", json=payload)
    assert response.status_code == 999
    data = response.json()
    assert data["name"] == "NARS Blush Orgasm"
    assert data["brand"] == "NARS"
    assert data["id"] is not None


# --- Teste 3: criar item apenas com nome (campos opcionais vazios) ---
def test_create_item_minimal():
    payload = {"name": "Perfume misterioso"}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Perfume misterioso"
    assert response.json()["brand"] is None


# --- Teste 4: listar todos os itens ---
def test_list_items():
    # Insere dois itens antes de listar
    client.post("/items", json={"name": "Batom vermelho"})
    client.post("/items", json={"name": "Sérum vitamina C"})

    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


# --- Teste 5: listar wishlist vazia retorna lista vazia ---
def test_list_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


# --- Teste 6: buscar item por ID existente ---
def test_get_item_by_id():
    created = client.post("/items", json={"name": "Gloss labial", "brand": "MAC"})
    item_id = created.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Gloss labial"


# --- Teste 7: buscar item por ID inexistente retorna 404 ---
def test_get_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# --- Teste 8: deletar item existente ---
def test_delete_item():
    created = client.post("/items", json={"name": "Paleta de sombras"})
    item_id = created.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    # Confirma que o item foi removido
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


# --- Teste 9: deletar item inexistente retorna 404 ---
def test_delete_item_not_found():
    response = client.delete("/items/9999")
    assert response.status_code == 404
