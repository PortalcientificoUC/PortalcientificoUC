# scraper.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# ==============================================================================
# FUNÇÕES DE BUSCA (SCRAPERS)
# Cada função é especializada em extrair dados de um site específico.
# Esta é a seção que pode precisar de manutenção se os sites mudarem.
# ==============================================================================

def fetch_fapeam_editais(url, fonte):
    """Busca editais no site da FAPEAM (Amazonas)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.find_all('article', class_='post-box', limit=3):
            titulo_tag = item.find('h2', class_='post-title')
            if titulo_tag and titulo_tag.find('a'):
                titulo = titulo_tag.text.strip()
                link = titulo_tag.find('a')['href']
                resumo = item.find('div', class_='entry-content').text.strip().split('Leia mais')[0]
                data = item.find('span', class_='date').text.strip() if item.find('span', 'date') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_fapespa_editais(url, fonte):
    """Busca editais no site da FAPESPA (Pará)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.find_all('div', class_='conteudo-lista__item', limit=3):
            titulo_tag = item.find('h3', class_='conteudo-lista__titulo')
            if titulo_tag and item.find('a'):
                titulo = titulo_tag.text.strip()
                link = "https://www.fapespa.pa.gov.br" + item.find('a')['href']
                resumo = item.find('p', class_='conteudo-lista__resumo').text.strip() if item.find('p', 'conteudo-lista__resumo') else "Sem resumo."
                data = item.find('span', class_='conteudo-lista__data').text.strip() if item.find('span', 'conteudo-lista__data') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_fapac_editais(url, fonte):
    """Busca editais no site da FAPAC (Acre)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('article.elementor-post', limit=3):
            titulo_tag = item.select_one('h3.elementor-post__title a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link = titulo_tag['href']
                resumo = item.select_one('div.elementor-post__excerpt p').text.strip() if item.select_one('div.elementor-post__excerpt p') else "Sem resumo."
                data = item.select_one('span.elementor-post-date').text.strip() if item.select_one('span.elementor-post-date') else "Data não encontrada"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_cnpq_editais(url, fonte):
    """Busca editais no site do CNPq."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for item in soup.select('div.call-item-content', limit=3):
            titulo_tag = item.select_one('h3 a')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link = titulo_tag['href']
                resumo = item.select_one('p').text.strip() if item.select_one('p') else "Sem resumo."
                # O site do CNPq não tem data visível na lista principal
                data = "Verificar no link"
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_fapdf_editais(url, fonte):
    """Busca editais no site da FAPDF (Distrito Federal)."""
    try:
        print(f"Buscando em: {fonte}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        # O site da FAPDF usa tabelas
        for row in soup.select('table tbody tr', limit=3):
            cells = row.find_all('td')
            if len(cells) >= 2:
                titulo_tag = cells[1].find('a')
                if titulo_tag:
                    titulo = titulo_tag.text.strip()
                    link = titulo_tag['href']
                    resumo = f"Edital {cells[0].text.strip()}."
                    data = "Verificar no link"
                    editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": fonte})
        print(f"-> Encontrados {len(editais)} editais.")
        return editais
    except Exception as e:
        print(f"-> Erro ao buscar em {fonte}: {e}")
        return []

def fetch_placeholder(url, fonte):
    """Função modelo para sites que ainda não foram implementados."""
    print(f"Buscando em: {fonte} (ainda não implementado).")
    # Para implementar, um desenvolvedor precisaria analisar o site
    # e escrever o código de extração aqui.
    return []


# ==============================================================================
# LISTA CENTRAL DE FONTES
# Para adicionar um novo site, adicione um dicionário a esta lista.
# ==============================================================================
FONTES_DE_BUSCA = [
    # Região Norte
    {"nome": "FAPEAM - Amazonas", "url": "http://www.fapeam.am.gov.br/editais/", "funcao_busca": fetch_fapeam_editais},
    {"nome": "FAPESPA - Pará", "url": "https://www.fapespa.pa.gov.br/pt-br/editais", "funcao_busca": fetch_fapespa_editais},
    {"nome": "FAPAC - Acre", "url": "https://fapac.ac.gov.br/editais/", "funcao_busca": fetch_fapac_editais},
    {"nome": "FAPEAP - Amapá", "url": "https://fapeap.portal.ap.gov.br/", "funcao_busca": fetch_placeholder},
    {"nome": "FAPT - Tocantins", "url": "https://www.to.gov.br/fapt/chamadas-publicas", "funcao_busca": fetch_placeholder},
    {"nome": "FAPERO - Rondônia", "url": "https://rondonia.ro.gov.br/fapero/", "funcao_busca": fetch_placeholder},
    {"nome": "FAPERR - Roraima", "url": "https://www.faperr.rr.gov.br/", "funcao_busca": fetch_placeholder},
    # Região Centro-Oeste
    {"nome": "FAPEMAT - Mato Grosso", "url": "https://www.fapemat.mt.gov.br/", "funcao_busca": fetch_placeholder},
    {"nome": "FAPEG - Goiás", "url": "https://goias.gov.br/fapeg/", "funcao_busca": fetch_placeholder},
    {"nome": "FUNDECT - Mato Grosso do Sul", "url": "https://www.fundect.ms.gov.br/", "funcao_busca": fetch_placeholder},
    {"nome": "FAPDF - Distrito Federal", "url": "https://www.fap.df.gov.br/editais-abertos/", "funcao_busca": fetch_fapdf_editais},
    # Nacionais
    {"nome": "CAPES", "url": "https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/bolsas/bolsas-e-auxilios-a-pesquisa/editais-capes", "funcao_busca": fetch_placeholder},
    {"nome": "CNPq", "url": "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/chamadas-publicas", "funcao_busca": fetch_cnpq_editais},
    {"nome": "FINEP", "url": "https://www.finep.gov.br/chamadas-publicas", "funcao_busca": fetch_placeholder},
    {"nome": "CONFAP", "url": "https://confap.org.br/pt/chamadas", "funcao_busca": fetch_placeholder},
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
