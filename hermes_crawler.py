import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# ✅ URL da API Hermes que retorna links e títulos
API_DOCUMENTOS_URL = "https://bolder-hot-hockey.glitch.me/anbima/documentos"
PASTA_SAIDA = "documentos"
BASE_SITE_ANBIMA = "https://www.anbima.com.br"

# ✅ Cria a pasta se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

def limpar_nome_arquivo(titulo):
    """Remove caracteres inválidos para nome de arquivo"""
    return re.sub(r"[^\w\s-]", "", titulo).strip().replace(" ", "_") + ".txt"

def extrair_texto_da_url(url):
    """Baixa o HTML e extrai o texto limpo"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove scripts, estilos, navbars, etc.
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
        link_original = doc.get("link")

        if not link_original or link_original.startswith("#"):
            continue

        # 🔗 Corrige links relativos
        link = urljoin(BASE_SITE_ANBIMA, link_original)

        nome_arquivo = limpar_nome_arquivo(titulo)
        caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

        print(f"⬇️  Baixando: {titulo}")
        texto = extrair_texto_da_url(link)

        if texto:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"✅ Salvo: {caminho}")
        else:
            print(f"⚠️ Falhou ao extrair: {titulo} ({link})")

    print("\n🏁 Coleta finalizada!")

if __name__ == "__main__":
    baixar_documentos()

