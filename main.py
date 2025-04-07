from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API ONLINE - ROTA / FUNCIONANDO"

@app.route("/anbima/documentos")
def rota_documentos():
    return "✅ API ONLINE - ROTA /anbima/documentos FUNCIONANDO"
