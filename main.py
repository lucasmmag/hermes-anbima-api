from flask import Flask, jsonify

import requests

from bs4 import BeautifulSoup

import os

 

app = Flask(__name__)

 

@app.route("/")

def index():
    print("✅ Rota raiz acessada")
    return "Hermes ANBIMA API está rodando 🤖⚖️"

 

@app.route("/anbima/documentos", methods=["GET"], strict_slashes=False)

def buscar_documentos():
    print("✅ Função buscar_documentos foi chamada!")

 

    BASE_URL = "https://www.anbima.com.br/pt_br/autorregular/autorregular.htm"

    HEADERS = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    }

 

    try:

        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)

        response.raise_for_status()

    except Exception as e:

        print(f"❌ Erro ao acessar a página da ANBIMA: {e}")

        return jsonify({"erro": "Não foi possível acessar a ANBIMA"}), 500

 

    soup = BeautifulSoup(response.text, "html.parser")

    documentos = []

 

    for link in soup.select("a[href^='/pt_br/autorregular/']"):

        href = link.get("href")

        titulo = link.get_text(strip=True)

        if href and titulo:

            documentos.append({

                "titulo": titulo,

                "url": f"https://www.anbima.com.br{href}"

            })

 

    print(f"🔍 {len(documentos)} documentos encontrados.")

    return jsonify({"resultados": documentos})

 

if __name__ == "__main__":

    print("🚀 Aplicação Flask está rodando...")

    port = int(os.environ.get("PORT", 3000))

    app.run(host="0.0.0.0", port=port)