from flask import Flask, render_template
import dapr.clients
import os
import requests

app = Flask(__name__)
dapr_client = dapr.clients.DaprClient()

def executar_sql(declaracao_sql, *parametros):
    resposta = dapr_client.invoke_binding(
        binding_name="postgres-db",
        operation="exec",
        data={
            "query": declaracao_sql,
            "params": parametros
        }
    )
    return resposta.json()

def sql_output(provedor):
    with dapr_client:
        sqlCmd = (f'SELECT * FROM providers WHERE nome_provedor = "{provedor}"')
        payload = {'sql': sqlCmd}

        print(sqlCmd, flush=True)

        try:
            # Insert order using Dapr output binding via HTTP Post
            resp = dapr_client.invoke_binding(binding_name="postgres-db", operation='exec',
                                    binding_metadata=payload, data='')
            return resp
        except Exception as e:
            print(e, flush=True)
            raise SystemExit(e)

def executar_sql_query(provedor):
    sqlcmd_ = f'"SELECT * FROM providers WHERE nome_provedor = \'{provedor}\'"'
    sqlcmd = '\'{ "sql": ' + sqlcmd_ + ' }\''
    resposta = dapr_client.invoke_binding(
        binding_name="postgres-db",
        operation="query",
        metadata=sqlcmd
    )
    return resposta

   


@app.route("/")
def home():
    meu_provedor = os.environ.get('PROVEDOR')
    #resultado = sql_output(meu_provedor)
    #resultado = executar_sql("SELECT * FROM providers WHERE nome_provedor = $1", provedor)
    resultado = executar_sql_query(meu_provedor)
    print(type(resultado))
    print(resultado)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
