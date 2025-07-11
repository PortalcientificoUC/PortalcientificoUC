# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_fapeam_editais():
    """Busca editais no site da FAPEAM (Amazonas)."""
    try:
        url = "http://www.fapeam.am.gov.br/editais/"
        print(f"Buscando editais em: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for edital_tag in soup.find_all('article', class_='post-box', limit=5):
            titulo_tag = edital_tag.find('h2', class_='post-title')
            link_tag = titulo_tag.find('a') if titulo_tag else None
            resumo_tag = edital_tag.find('div', class_='entry-content')
            if titulo_tag and link_tag and resumo_tag:
                titulo = titulo_tag.text.strip()
                link = link_tag['href']
                resumo = resumo_tag.text.strip().split('Leia mais')[0]
                data_tag = edital_tag.find('span', class_='date')
                data = data_tag.text.strip() if data_tag else datetime.now().strftime('%d/%m/%Y')
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": "FAPEAM - Amazonas"})
        print(f"Encontrados {len(editais)} editais na FAPEAM.")
        return editais
    except Exception as e:
        print(f"Erro ao buscar editais da FAPEAM: {e}")
        return []

def fetch_fapespa_editais():
    """Busca editais no site da FAPESPA (Pará)."""
    try:
        url = "https://www.fapespa.pa.gov.br/pt-br/editais"
        print(f"Buscando editais em: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        editais = []
        for edital_tag in soup.find_all('div', class_='conteudo-lista__item', limit=5):
            titulo_tag = edital_tag.find('h3', class_='conteudo-lista__titulo')
            link_tag = edital_tag.find('a')
            resumo_tag = edital_tag.find('p', class_='conteudo-lista__resumo')
            if titulo_tag and link_tag:
                titulo = titulo_tag.text.strip()
                link = "https://www.fapespa.pa.gov.br" + link_tag['href']
                resumo = resumo_tag.text.strip() if resumo_tag else "Sem resumo disponível."
                data_tag = edital_tag.find('span', class_='conteudo-lista__data')
                data = data_tag.text.strip() if data_tag else datetime.now().strftime('%d/%m/%Y')
                editais.append({"titulo": titulo, "data": data, "resumo": resumo, "link": link, "fonte": "FAPESPA - Pará"})
        print(f"Encontrados {len(editais)} editais na FAPESPA.")
        return editais
    except Exception as e:
        print(f"Erro ao buscar editais da FAPESPA: {e}")
        return []

if __name__ == "__main__":
    todos_editais = []
    todos_editais.extend(fetch_fapeam_editais())
    todos_editais.extend(fetch_fapespa_editais())
    print(f"Total de editais encontrados: {len(todos_editais)}")
    with open('editais.json', 'w', encoding='utf-8') as f:
        json.dump(todos_editais, f, ensure_ascii=False, indent=4)
    print("Arquivo 'editais.json' foi atualizado com sucesso.")
