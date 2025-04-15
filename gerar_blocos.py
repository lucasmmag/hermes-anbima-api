import os
import json
import re

# Caminho da pasta com os arquivos .txt
PASTA_DOCUMENTOS = "documentos"
PASTA_SAIDA = "blocos_indexados"
os.makedirs(PASTA_SAIDA, exist_ok=True)

def dividir_em_blocos(documento_nome, conteudo, tamanho_bloco=5):
    linhas = conteudo.splitlines()
    blocos = []
    buffer = []
    inicio_linha = 0

    for i, linha in enumerate(linhas):
        if linha.strip():  # ignora linhas em branco
            buffer.append(linha.strip())

        if len(buffer) >= tamanho_bloco or (linha.strip() == "" and buffer):
            bloco_texto = " ".join(buffer)
            blocos.append({
                "documento": documento_nome,
                "linha_inicio": inicio_linha + 1,
                "linha_fim": i + 1,
                "conteudo": bloco_texto
            })
            buffer = []
            inicio_linha = i + 1

    if buffer:
        bloco_texto = " ".join(buffer)
        blocos.append({
            "documento": documento_nome,
            "linha_inicio": inicio_linha + 1,
            "linha_fim": len(linhas),
            "conteudo": bloco_texto
        })

    return blocos

# Processa todos os arquivos .txt da pasta
todos_blocos = []
for nome_arquivo in os.listdir(PASTA_DOCUMENTOS):
    if nome_arquivo.endswith(".txt"):
        caminho = os.path.join(PASTA_DOCUMENTOS, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()
            blocos = dividir_em_blocos(nome_arquivo, texto)
            todos_blocos.extend(blocos)

# Salva os blocos em formato JSONL
saida = os.path.join(PASTA_SAIDA, "blocos_anbima.jsonl")
with open(saida, "w", encoding="utf-8") as out:
    for bloco in todos_blocos:
        json.dump(bloco, out, ensure_ascii=False)
        out.write("\n")

print(f"✅ {len(todos_blocos)} blocos salvos em {saida}")
