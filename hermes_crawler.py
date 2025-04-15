import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# URL da sua API Hermes (que lista os documentos)
API_DOCUMENTOS_URL = "https://bolder-hot-hockey.glitch.me/anbima/documentos"
BASE_SITE_ANBIMA = "https://www.anbima.com.br"
PASTA_SAIDA = "documentos"

# Palavras-chave para filtrar documentos relevantes
PALAVRAS_CHAVE = [
    "código", "norma", "regra", "manual", "lei", "artigo", "circular",
    "comunicado", "supervisão", "ofício", "autorregulação", "penalidade",
    "adesão", "procedimento", "orientação", "guia", "regulação"
]

# Garante que a pasta de saída exista
os.makedirs(PASTA_SAIDA, exist_ok=True)

def limpar_nome_arquivo(titulo):
    """Remove caracteres inválidos para nomes de arquivo"""
    return re.sub(r"[^\w\s-]", "", titulo).strip().replace(" ", "_") + ".txt"

def contem_palavra_chave(texto):
    """Verifica se o texto contém alguma palavra-chave relevante"""
    texto = texto.lower()
    return any(p in texto for p in PALAVRAS_CHAVE)

def extrair_texto_da_url(url):
    """Acessa a URL e extrai o texto da página"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove elementos não relevantes
        for tag in soup(["script", "style", "header", "footer", "nav"]):
            tag.decompose()

        return soup.get_text(separator="\n", strip=True)

    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return None

def baixar_documentos():
    print("🔄 Buscando documentos da API Hermes...")

    try:
        resposta = requests.get(API_DOCUMENTOS_URL, timeout=10)
        resposta.raise_for_status()
        documentos = resposta.json()
    except Exception as e:
        print(f"❌ Erro ao buscar documentos: {e}")
        return

    print(f"📄 {len(documentos)} documentos encontrados.\n")

    for doc in documentos:
        titulo = doc.get("titulo", "documento")
        link_raw = doc.get("link")

        if not link_raw or link_raw.startswith("#") or "mailto:" in link_raw:
            continue

        # Ignora domínios externos indesejados
        if "zendesk" in link_raw or "partiuinvestir" in link_raw:
            continue

        # Corrige links relativos
        url = urljoin(BASE_SITE_ANBIMA, link_raw)

        if not contem_palavra_chave(titulo) and not contem_palavra_chave(url):
            print(f"⏩ Ignorado (irrelevante): {titulo}")
            continue

        nome_arquivo = limpar_nome_arquivo(titulo)
        caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

        print(f"⬇️  Baixando: {titulo}")
        texto = extrair_texto_da_url(url)

        if texto:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"✅ Salvo: {caminho}")
        else:
            print(f"⚠️ Falhou ao extrair: {url}")

    print("\n🏁 Coleta concluída com sucesso!")

if __name__ == "__main__":
    baixar_documentos()
