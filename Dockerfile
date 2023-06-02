# Define a imagem base
FROM python:3.9-slim

RUN apt-get update
RUN apt-get install telnet netcat iputils-ping curl postgresql-client -y
#RUN curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de código-fonte para o diretório de trabalho

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
CMD ["flask", "run", "--host", "0.0.0.0", "--debug"]
#CMD ["dapr", "run", "--app-id", "myapp", "--app-port", "5000", "--", "flask", "run", "--host", "0.0.0.0", "--debug"]

