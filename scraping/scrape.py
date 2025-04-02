import requests
from bs4 import BeautifulSoup
import os
from database.database import insert_into_db  # Importando a função do módulo database.py

# URL do site
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

# Função para baixar PDFs
def download_pdf(pdf_url, folder):
    response = requests.get(pdf_url)
    filename = pdf_url.split("/")[-1]
    filepath = os.path.join(folder, filename)

    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f'{filename} baixado com sucesso!')

    # Inserir no banco de dados
    insert_into_db(filename, pdf_url)

    return filepath

# Função principal
def scrape_pdfs():
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pdfs')
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Erro ao acessar a página!")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = list(set(a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')))
    print(f'Encontrados {len(pdf_links)} arquivos PDF.')

    for link in pdf_links:
        if not link.startswith('http'):
            link = 'https://www.gov.br' + link
        download_pdf(link, folder)
