from flask import Flask, render_template
import dapr.clients
import os
import json
import logging


app = Flask(__name__)

def executar_sql(declaracao_sql, *parametros):
    dapr_client = dapr.clients.DaprClient()
    resposta = dapr_client.invoke_binding(
        binding_name="postgres-db",
        operation="exec",
        data={
            "query": declaracao_sql,
            "params": parametros
        }
    )
    return resposta.data.json()

def sql_output(provedor):
    dapr_client = dapr.clients.DaprClient()
    with dapr_client:
        sqlCmd = (f"SELECT companhia FROM providers WHERE nome_provedor='{provedor}'")
        payload = {'sql': sqlCmd}
        try:
            resp_ = dapr_client.invoke_binding(binding_name="postgres-db", operation='query', binding_metadata=payload, data='')
            resp_dict = json.loads(resp_.data.decode('utf-8'))
            resp = [f'{resp_dict[0][0]} é a companhia proprietária do provedor de cloud {provedor} !']          
            return [resp]
        except Exception as e:
            print(e, flush=True)
            raise SystemExit(e)

  
@app.route("/")
def home():
    meu_provedor = os.environ.get('PROVEDOR')
    #resultado = sql_output(meu_provedor)
    resultado = executar_sql("SELECT companhia FROM providers WHERE nome_provedor=%1", meu_provedor)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
