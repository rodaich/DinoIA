# Usa a imagem oficial do Python
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080
EXPOSE 8080

# Comando para iniciar o servidor
CMD ["python", "main.py"]
