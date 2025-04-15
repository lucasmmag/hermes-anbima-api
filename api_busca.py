from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import json

# Configuração do app
app = Flask(__name__)
CORS(app)

# Carrega os blocos indexados
with open("blocos_anbima.jsonl", "r", encoding="utf-8") as f:
    blocos = [json.loads(linha) for linha in f]

# Carrega modelo leve de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Gera embeddings para os blocos
corpus = [bloco["conteudo"] for bloco in blocos]
embeddings_corpus = modelo.encode(corpus, convert_to_tensor=True)

@app.route("/")
def home():
    return "✅ API Hermes online!"

@app.route("/buscar", methods=["GET"])
def buscar():
    pergunta = request.args.get("pergunta")
    if not pergunta:
        return jsonify({"erro": "Parâmetro 'pergunta' não fornecido"}), 400

    embedding_pergunta = modelo.encode(pergunta, convert_to_tensor=True)
    resultados = util.semantic_search(embedding_pergunta, embeddings_corpus, top_k=5)[0]

    blocos_encontrados = [
        {
            "score": round(hit["score"], 3),
            "trecho": blocos[hit["corpus_id"]]["conteudo"]
        }
        for hit in resultados
    ]

    return jsonify({"pergunta": pergunta, "respostas": blocos_encontrados})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
