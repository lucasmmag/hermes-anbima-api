import requests
from bs4 import BeautifulSoup
import os
import re

# URL da sua API que retorna os documentos
API_DOCUMENTOS_URL = "https://bolder-hot-hockey.glitch.me/anbima/documentos"
PASTA_SAIDA = "documentos"

# Cria a pasta se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

def limpar_nome_arquivo(titulo):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r"[^\w\s-]", "", titulo).strip().replace(" ", "_") + ".txt"

def extrair_texto_da_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        textos = soup.stripped_strings
        return "\n".join(textos)
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
        return None

def baixar_documentos():
    print("🔄 Buscando lista de documentos da API Hermes...")
    try:
        resposta = requests.get(API_DOCUMENTOS_URL, timeout=10)
        resposta.raise_for_status()
        documentos = resposta.json()
    except Exception as e:
        print(f"❌ Erro ao buscar documentos: {e}")
        return

    print(f"📄 {len(documentos)} documentos encontrados. Iniciando download...\n")

    for doc in documentos:
        titulo = doc.get("titulo", "documento")
        link = doc.get("link")

        if not link:
            continue

        nome_arquivo = limpar_nome_arquivo(titulo)
        caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

        print(f"⬇️  Baixando: {titulo}")
        texto = extrair_texto_da_url(link)

        if texto:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"✅ Salvo em: {caminho}")
        else:
            print(f"⚠️ Falhou ao extrair: {titulo}")

    print("\n🏁 Coleta finalizada!")

if __name__ == "__main__":
    baixar_documentos()
