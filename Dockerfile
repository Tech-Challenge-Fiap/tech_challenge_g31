# Use a imagem base do Python para desenvolvimento
FROM python:3.8-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

COPY system system
COPY app.py .

# Instale as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a aplicação Flask será executada (geralmente 5000)
EXPOSE 5000

# Comando para iniciar a aplicação Flask em modo de desenvolvimento
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
