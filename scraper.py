# scraper.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from urllib.parse import urljoin

# ==============================================================================
# FUNÇÃO AUXILIAR
# Para garantir que todos os links sejam completos (absolutos).
# ==============================================================================
def make_absolute_url(base_url, link):
    """Converte um link relativo em um link absoluto."""
    return urljoin(base_url, link)

# ==============================================================================
# FUNÇÕES DE BUSCA (SCRAPERS)
# Cada função é especializada em extrair dados de um site específico.
# ==============================================================================

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
                link_relativo = titulo_tag['href']
                link_absoluto = make_absolute_url(base_url, link_relativo)
                resumo = item.select_one('div.elementor-post__excerpt p').text.strip() if item.select_one('div.elementor-post__excerpt p') else "Sem resumo."
                data = item.select_one('span.elementor-post-date').text.strip() if item.select_one('span.elementor-post-date') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link_absoluto, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_fapemat_editais(url, fonte):
    """Busca editais no site da FAPEMAT (Mato Grosso)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        base_url = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('div.card-edital', limit=3):
            titulo_tag = item.select_one('h4.card-title a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link_relativo = titulo_tag['href']
                link_absoluto = make_absolute_url(base_url, link_relativo)
                resumo = item.select_one('p.card-text').text.strip() if item.select_one('p.card-text') else "Sem resumo."
                data = item.select_one('small.text-muted').text.strip() if item.select_one('small.text-muted') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link_absoluto, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_fapeg_editais(url, fonte):
    """Busca editais no site da FAPEG (Goiás)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        base_url = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('article.post', limit=3):
            titulo_tag = item.select_one('h2.entry-title a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link_relativo = titulo_tag['href']
                link_absoluto = make_absolute_url(base_url, link_relativo)
                resumo = item.select_one('div.entry-content p').text.strip() if item.select_one('div.entry-content p') else "Sem resumo."
                data = item.select_one('span.entry-date').text.strip() if item.select_one('span.entry-date') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link_absoluto, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_fundect_editais(url, fonte):
    """Busca editais no site da FUNDECT (Mato Grosso do Sul)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        base_url = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('div.edital-item', limit=3):
            titulo_tag = item.select_one('h4.edital-title a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link_relativo = titulo_tag['href']
                link_absoluto = make_absolute_url(base_url, link_relativo)
                resumo = item.select_one('p').text.strip() if item.select_one('p') else "Sem resumo."
                data = "Verificar no link"
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
                link_relativo = titulo_tag['href']
                link_absoluto = make_absolute_url(base_url, link_relativo)
                resumo = item.select_one('p').text.strip() if item.select_one('p') else "Sem resumo."
                data = "Verificar no link"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link_absoluto, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_placeholder(url, fonte):
    """Função modelo para sites que ainda não foram implementados por serem complexos."""
    print(f"Buscando em: {fonte} (site complexo, ainda não implementado).")
    return []


# ==============================================================================
# LISTA CENTRAL DE FONTES
# Esta é a nova lista de sites que o robô irá verificar.
# ==============================================================================
FONTES_DE_BUSCA = [
    {"nome": "FAPERO - Rondônia", "url": "https://rondonia.ro.gov.br/fapero/", "funcao_busca": fetch_placeholder},
    {"nome": "FAPAC - Acre", "url": "https://fapac.ac.gov.br/editais/", "funcao_busca": fetch_fapac_editais},
    {"nome": "FAPEMAT - Mato Grosso", "url": "https://www.fapemat.mt.gov.br/editais", "funcao_busca": fetch_fapemat_editais},
    {"nome": "FAPEG - Goiás", "url": "https://goias.gov.br/fapeg/category/chamadas-publicas/", "funcao_busca": fetch_fapeg_editais},
    {"nome": "FUNDECT - Mato Grosso do Sul", "url": "https://www.fundect.ms.gov.br/editais/", "funcao_busca": fetch_fundect_editais},
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

    for fonte_info in FONTES_DE_BUSCA:
        # Chama a função de busca designada para cada site
        resultados = fonte_info["funcao_busca"](fonte_info["url"], fonte_info["nome"])
        todos_editais.extend(resultados)
    
    print("-" * 30)
    print(f"Busca finalizada. Total de editais encontrados: {len(todos_editais)}")
    
    # Salva os dados em um arquivo JSON
    with open('editais.json', 'w', encoding='utf-8') as f:
        json.dump(todos_editais, f, ensure_ascii=False, indent=4)
        
    print("Arquivo 'editais.json' foi atualizado com sucesso.")
