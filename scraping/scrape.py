import requests
from bs4 import BeautifulSoup
import zipfile
import os

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
    return filepath


# Função para compactar PDFs
def zip_files(file_paths, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            zipf.write(file, os.path.basename(file))
    print(f'Arquivos compactados para {zip_name}')


# Função principal
def main():
    # Criar pasta para armazenar PDFs
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pdfs')
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Baixar e extrair links para PDFs
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Erro ao acessar a página!")
        return  # Encerra a execução caso a requisição falhe

    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar todos os links de PDFs
    pdf_links = list(set(a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')))
    print(f'Encontrados {len(pdf_links)} arquivos PDF.')

    # Baixar PDFs
    downloaded_files = []
    for link in pdf_links:
        if not link.startswith('http'):
            link = 'https://www.gov.br' + link
        file_path = download_pdf(link, folder)
        downloaded_files.append(file_path)

        # Compactar PDFs na pasta correta
    zip_path = os.path.join(os.path.dirname(folder), 'rol_procedimentos.zip')
    zip_files(downloaded_files, zip_path)

if __name__ == "__main__":
    main()
