# indexador.py
import json
import os
import faiss
import openai
from tqdm import tqdm
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (como a chave da OpenAI)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Caminho do seu arquivo de blocos
CAMINHO_BLOCOS = "blocos_anbima.jsonl"
# Arquivos gerados
CAMINHO_FAISS = "indice_anbima.faiss"
CAMINHO_METADADOS = "metadados.json"

# Função para gerar embeddings com a OpenAI
def gerar_embedding(texto: str):
    resposta = openai.Embedding.create(
        input=texto,
        model="text-embedding-3-small"
    )
    return resposta["data"][0]["embedding"]

def main():
    textos = []
    metadados = []

    print("📖 Lendo blocos do arquivo JSONL...")
    with open(CAMINHO_BLOCOS, "r", encoding="utf-8") as f:
        for linha in f:
            bloco = json.loads(linha.strip())
            texto = bloco.get("texto", "").strip()
            if texto:
                textos.append(texto)
                metadados.append(bloco)

    print(f"🔢 Gerando embeddings para {len(textos)} blocos...")
    vetores = []
    for texto in tqdm(textos):
        embedding = gerar_embedding(texto)
        vetores.append(embedding)

    print("🧠 Construindo índice FAISS...")
    dimensao = len(vetores[0])
    index = faiss.IndexFlatL2(dimensao)
    index.add(np.array(vetores).astype("float32"))

    print(f"💾 Salvando índice em '{CAMINHO_FAISS}'...")
    faiss.write_index(index, CAMINHO_FAISS)

    print(f"💾 Salvando metadados em '{CAMINHO_METADADOS}'...")
    with open(CAMINHO_METADADOS, "w", encoding="utf-8") as f:
        json.dump(metadados, f, ensure_ascii=False, indent=2)

    print("✅ Indexação concluída!")

if __name__ == "__main__":
    import numpy as np
    main()
