import os

PASTA_DOCUMENTOS = "documentos"

def carregar_documentos():
    base_conhecimento = []

    for nome_arquivo in os.listdir(PASTA_DOCUMENTOS):
        caminho = os.path.join(PASTA_DOCUMENTOS, nome_arquivo)

        if nome_arquivo.endswith(".txt"):
            with open(caminho, "r", encoding="utf-8") as f:
                texto = f.read()

            base_conhecimento.append({
                "titulo": nome_arquivo.replace(".txt", "").replace("_", " "),
                "conteudo": texto
            })

    return base_conhecimento

def buscar_resposta(pergunta, base_conhecimento):
    pergunta_lower = pergunta.lower()

    melhores_resultados = []

    for doc in base_conhecimento:
        conteudo = doc["conteudo"].lower()

        if any(palavra in conteudo for palavra in pergunta_lower.split()):
            melhores_resultados.append(doc)

    if not melhores_resultados:
        return "❌ Nenhum documento relevante encontrado."

    print(f"\n🔍 Resultados encontrados: {len(melhores_resultados)}")
    for doc in melhores_resultados:
        print(f"\n📄 Documento
