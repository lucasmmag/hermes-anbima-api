import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# URL da sua API Hermes que retorna links e títulos
API_DOCUMENTOS_URL = "https://bolder-hot-hockey.glitch.me/anbima/documentos"
BASE_SITE_ANBIMA = "https://www.anbima.com.br"
PASTA_SAIDA = "documentos"

# Cria a pasta se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

def limpar_nome_arquivo(titulo):
    """Remove caracteres inválidos para nomes de arquivo"""
    return re.sub(r"[^\w\s-]", "", titulo).strip().replace(" ", "_") + ".txt"

def extrair_texto_da_url(url):
    """Faz scraping do conteúdo de uma URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove elementos que não são conteúdo principal
        for tag in soup(["script", "style", "header", "footer", "nav"]):
            tag.decompose()

        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}")
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
        link_raw = doc.get("link")

        if not link_raw or link_raw.strip() == "#" or link_raw.lower().startswith("javascript"):
            print(f"⚠️ Ignorando link inválido: {link_raw}")
            continue

        # Corrige links relativos automaticamente
        url = urljoin(BASE_SITE_ANBIMA, link_raw)

        nome_arquivo = limpar_nome_arquivo(titulo)
        caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

        print(f"⬇️  Baixando: {titulo}")
        texto = extrair_texto_da_url(url)

        if texto:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"✅ Salvo: {caminho}")
        else:
            print(f"⚠️ Conteúdo não extraído: {url}")

    print("\n🏁 Coleta finalizada!")

if __name__ == "__main__":
    baixar_documentos()
