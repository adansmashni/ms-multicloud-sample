from flask import Flask, render_template
import dapr.clients
import os
import json

app = Flask(__name__)

def sql_output(provedor):
    dapr_client = dapr.clients.DaprClient()
    with dapr_client:
        sqlCmd = (f"SELECT companhia FROM providers WHERE nome_provedor='{provedor}'")
        payload = {'sql': sqlCmd}
        try:
            resp_ = dapr_client.invoke_binding(binding_name="postgres-db", operation='query', binding_metadata=payload, data='')
            resp_dict = json.loads(resp_.data.decode('utf-8'))
            resp = [f'{resp_dict[0][0]} é a companhia proprietária do provedor de cloud {provedor} !']          
            return [resp[0]]
        except Exception as e:
            print(e, flush=True)
            raise SystemExit(e)
  
@app.route("/")
def home():
    meu_provedor = os.environ.get('PROVEDOR')
    #resultado = sql_output(meu_provedor)
    resultado = ['Microsoft']
    return render_template("index.html", resultado=resultado, provedor=meu_provedor)

if __name__ == "__main__":
    app.run(debug=True)
