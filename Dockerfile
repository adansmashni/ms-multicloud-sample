# Define a imagem base
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de código-fonte para o diretório de trabalho
RUN curl -fsSL -o get-dapr.sh https://raw.githubusercontent.com/dapr/cli/master/install/install.sh \
    && chmod +x get-dapr.sh \
    && DAPR_INSTALL_VERSION=1.4.0 ./get-dapr.sh

COPY requirements.txt /app
COPY src /app

# Define as variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta em que a aplicação Flask está sendo executada
EXPOSE 5000

# Comando para executar a aplicação Flask
CMD ["dapr", "run", "--app-id", "myapp", "--app-port", "5000", "flask", "run"]

