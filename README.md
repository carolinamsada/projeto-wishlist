# ✨ Glam Wishlist API 🛍️

> Sua lista de desejos — API REST para gerenciar os itens que você *precisa* (ou não) comprar.

![CI/CD](https://github.com/carolinamsada/projeto-wishlist/actions/workflows/ci.yml/badge.svg)

## 👥 Integrantes

Amanda Victória Almeida Silva

## 🛠️ Stack

- **Linguagem:** Python 3.11
- **Framework:** FastAPI
- **Banco de Dados:** SQLite (via SQLAlchemy)
- **Testes:** pytest + httpx (TestClient)
- **CI/CD:** GitHub Actions
- **Container:** Docker + Docker Hub

## 📦 Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Health check |
| POST | `/items` | Adiciona item à wishlist |
| GET | `/items` | Lista todos os itens |
| GET | `/items/{id}` | Busca item por ID |
| DELETE | `/items/{id}` | Remove item |

## 🚀 Como rodar localmente

### Com Docker Compose (recomendado)

```bash
docker compose up
```

Acesse: http://localhost:8000/docs

### Sem Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Rodar testes

```bash
pytest tests/ -v
```

## 🐳 Imagem Docker

```
docker pull SEU_USUARIO_DOCKERHUB/glam-wishlist:latest
```

🔗 [Ver no Docker Hub](https://hub.docker.com/r/SEU_USUARIO_DOCKERHUB/glam-wishlist)

## 📋 Pipeline CI/CD

O pipeline cobre:

- Build automático em push e PR na `main`
- Execução dos testes com falha automática em caso de erro
- Matriz de versões: Python 3.10 e 3.11
- Jobs paralelos (build + testes) com job de CD dependente
- Publicação de artefato de dependências
- Deploy de imagem Docker no Docker Hub (só na `main`)
- Secrets para credenciais sensíveis
