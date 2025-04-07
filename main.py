from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/")
def home():
    print("✅ Rota raiz acessada com sucesso")
    return "Hermes ANBIMA API está rodando 🔥⚖️"

@app.route("/anbima/documentos", methods=["GET"])
def buscar_documentos():
    print("✅ A rota /anbima/documentos foi chamada!")

    BASE_URL = "https://www.anbima.com.br/pt_br/autorregular/autorregular.htm"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao acessar ANBIMA: {e}")
        return jsonify({"erro": "Não foi possível acessar a página da ANBIMA"}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    documentos = []

    # Coletando todos os links da área de autorregulação
    for link in soup.select("a[href^='/pt_br/autorregular/']"):
        href = link.get("href")
        titulo = link.get_text(strip=True)
        if href and titulo:
            documentos.append({
                "titulo": titulo,
                "url": f"https://www.anbima.com.br{href}"
            })

    print(f"📄 {len(documentos)} documentos encontrados.")
    return jsonify({"resultados": documentos})

# Executado localmente (não afeta o Render)
if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 3000))
    print(f"🚀 Rodando localmente na porta {porta}")
    app.run(host="0.0.0.0", port=porta)
