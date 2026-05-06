# Imagem base enxuta — Python 3.11 slim reduz o tamanho final da imagem
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala dependências primeiro (aproveita cache do Docker nas builds seguintes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta que o uvicorn vai escutar
EXPOSE 8000

# Comando de inicialização da API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
