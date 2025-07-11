# scraper.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from urllib.parse import urljoin
import csv
import io

# ==============================================================================
# CONFIGURAÇÃO MANUAL
# Cole aqui o link da sua Planilha Google publicada como CSV.
# Ex: "https://docs.google.com/spreadsheets/d/e/seu-link/pub?output=csv"
# Se não quiser usar a planilha, deixe as aspas em branco.
# ==============================================================================
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQKZj7HPhKOQMxEG4F-dAEpeVis57gI4w77LT-1C8EjLaQb1gUHKQ2KU7OhCJ12x_UP2IFMkQBphxGb/pub?output=csv"

# ==============================================================================
# FUNÇÃO AUXILIAR
# Para garantir que todos os links sejam completos (absolutos).
# ==============================================================================
def make_absolute_url(base_url, link):
    """Converte um link relativo em um link absoluto."""
    return urljoin(base_url, link)

# ==============================================================================
# FUNÇÕES DE BUSCA (SCRAPERS)
# ==============================================================================

def fetch_google_sheet_editais(url):
    """Busca editais de uma planilha Google (formato CSV)."""
    if not url:
        print("URL da Planilha Google não configurada. Pulando esta etapa.")
        return []
    
    try:
        print("Buscando em: Planilha Google")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        
        # Usa o 'io.StringIO' para tratar o texto CSV como um arquivo em memória
        csv_file = io.StringIO(response.content.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        editais = []
        for row in reader:
            # Garante que as colunas existam no dicionário
            editais.append({
                "titulo": row.get("titulo", "Título não encontrado"),
                "data": row.get("data", "Data não encontrada"),
                "resumo": row.get("resumo", ""),
                "link": row.get("link", "#"),
                "fonte": row.get("fonte", "Planilha Manual")
            })
        print(f"-> Encontrados {len(editais)} editais na planilha.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar na Planilha Google: {e}")
        return []

def fetch_fapac_editais(url, fonte):
    """Busca editais no site da FAPAC (Acre)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        base_url = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('article.elementor-post', limit=3):
            titulo_tag = item.select_one('h3.elementor-post__title a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link_absoluto = make_absolute_url(base_url, titulo_tag['href'])
                resumo = item.select_one('div.elementor-post__excerpt p').text.strip() if item.select_one('div.elementor-post__excerpt p') else "Sem resumo."
                data = item.select_one('span.elementor-post-date').text.strip() if item.select_one('span.elementor-post-date') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link_absoluto, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_cnpq_editais(url, fonte):
    """Busca editais no site do CNPq."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        base_url = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('div.call-item-content', limit=3):
            titulo_tag = item.select_one('h3 a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link_absoluto = make_absolute_url(base_url, titulo_tag['href'])
                resumo = item.select_one('p').text.strip() if item.select_one('p') else "Sem resumo."
                data = "Verificar no link"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link_absoluto, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_placeholder(url, fonte):
    """Função modelo para sites que ainda não foram implementados."""
    print(f"Buscando em: {fonte} (site complexo, ainda não implementado).")
    return []

# ==============================================================================
# LISTA CENTRAL DE FONTES AUTOMÁTICAS
# ==============================================================================
FONTES_DE_BUSCA_AUTO = [
    {"nome": "FAPERO - Rondônia", "url": "https://rondonia.ro.gov.br/fapero/", "funcao_busca": fetch_placeholder},
    {"nome": "FAPAC - Acre", "url": "https://fapac.ac.gov.br/editais/", "funcao_busca": fetch_fapac_editais},
    {"nome": "FAPEMAT - Mato Grosso", "url": "https://www.fapemat.mt.gov.br/editais", "funcao_busca": fetch_placeholder}, # Site mudou, precisa de novo scraper
    {"nome": "FAPEG - Goiás", "url": "https://goias.gov.br/fapeg/category/chamadas-publicas/", "funcao_busca": fetch_placeholder}, # Site mudou
    {"nome": "FUNDECT - MS", "url": "https://www.fundect.ms.gov.br/editais/", "funcao_busca": fetch_placeholder}, # Site mudou
    {"nome": "CAPES", "url": "https://www.gov.br/capes/pt-br", "funcao_busca": fetch_placeholder},
    {"nome": "CNPq", "url": "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/chamadas-publicas", "funcao_busca": fetch_cnpq_editais},
    {"nome": "FINEP", "url": "http://www.finep.gov.br/chamadas-publicas", "funcao_busca": fetch_placeholder},
]

# ==============================================================================
# EXECUÇÃO PRINCIPAL DO ROBÔ
# ==============================================================================
if __name__ == "__main__":
    print("Iniciando robô de busca de editais...")
    todos_editais = []

    # 1. Busca os editais dos sites automáticos
    print("\n--- Buscando em fontes automáticas ---")
    for fonte_info in FONTES_DE_BUSCA_AUTO:
        resultados = fonte_info["funcao_busca"](fonte_info["url"], fonte_info["nome"])
        todos_editais.extend(resultados)
    
    # 2. Busca os editais da planilha manual
    print("\n--- Buscando em fonte manual (Planilha Google) ---")
    editais_manuais = fetch_google_sheet_editais(GOOGLE_SHEET_CSV_URL)
    todos_editais.extend(editais_manuais)

    print("-" * 30)
    print(f"Busca finalizada. Total de editais combinados: {len(todos_editais)}")
    
    # Salva os dados combinados em um arquivo JSON
    with open('editais.json', 'w', encoding='utf-8') as f:
        json.dump(todos_editais, f, ensure_ascii=False, indent=4)
        
    print("Arquivo 'editais.json' foi atualizado com sucesso.")
