from flask import Flask, render_template
import dapr.clients
import os



app = Flask(__name__)
dapr_client = dapr.clients.DaprClient()

def executar_sql(declaracao_sql, *parametros):
    resposta = dapr_client.invoke_binding(
        name="postgres-db",
        operation="exec",
        data={
            "query": declaracao_sql,
            "params": parametros
        }
    )
    return resposta.json()

@app.route("/")
def home():
    provedor = os.environ.get('PROVEDOR')
    resultado = executar_sql("SELECT * FROM providers WHERE nome_provedor = $1", provedor)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
