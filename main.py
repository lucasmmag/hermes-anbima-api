from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API ONLINE - ROTA / FUNCIONANDO"

@app.route("/anbima/documentos")
def rota_documentos():
    return "✅ API ONLINE - ROTA /anbima/documentos FUNCIONANDO"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
