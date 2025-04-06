from flask import Flask, jsonify

import requests

from bs4 import BeautifulSoup

import os

 

app = Flask(__name__)

 

# Rota de saúde (root) — evita que o Render derrube o app

@app.route("/")

def index():

    return "Hermes ANBIMA API está rodando 🧠⚖️"

 

# Rota principal: retorna documentos da ANBIMA

@app.route("/anbima/documentos", methods=["GET"])

def buscar_documentos():

    BASE_URL = "https://www.anbima.com.br/pt_br/autorregular/autorregular.htm"

    HEADERS = {"User-Agent": "Mozilla/5.0"}

 

    response = requests.get(BASE_URL, headers=HEADERS)

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

 

    return jsonify({"resultados": documentos})

 

# Inicializa o app no Render

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 3000))

    app.run(host="0.0.0.0", port=port)

