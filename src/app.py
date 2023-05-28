from flask import Flask, render_template
import dapr.clients

app = Flask(__name__)
dapr_client = dapr.clients.DaprClient()

def executar_sql(declaracao_sql, *parametros):
    resposta = dapr_client.invoke_binding(
        name="nome_do_binding_postgresql",
        operation="exec",
        data={
            "query": declaracao_sql,
            "params": parametros
        }
    )
    return resposta.json()

@app.route("/")
def home():
    provedor = "provedor_a"
    resultado = executar_sql("SELECT * FROM providers WHERE nome_provedor = $1", provedor)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
