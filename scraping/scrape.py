import requests
from bs4 import BeautifulSoup
import os
import zipfile
from database.database import insert_into_db  # Importa a função que insere registros no banco de dados

# Define a URL da página que contém os PDFs a serem baixados
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

# Define a pasta onde os PDFs serão armazenados
folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'pdfs')

# Se a pasta ainda não existir, cria ela automaticamente
if not os.path.exists(folder):
    os.makedirs(folder)


# Função para baixar um arquivo PDF e salvar na pasta especificada
def download_pdf(pdf_url, folder):
    response = requests.get(pdf_url)  # Faz a requisição para baixar o arquivo
    filename = pdf_url.split("/")[-1]  # Extrai o nome do arquivo a partir da URL
    filepath = os.path.join(folder, filename)  # Define o caminho completo do arquivo

    # Salva o arquivo baixado no diretório especificado
    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f'{filename} baixado com sucesso!')

    # Insere os detalhes do arquivo no banco de dados
    insert_into_db(filename, pdf_url)

    return filepath  # Retorna o caminho do arquivo baixado


# Função para compactar todos os arquivos PDF da pasta em um único arquivo ZIP
def compactar_pdfs(folder, zip_name):
    zip_path = os.path.join(folder, zip_name)  # Define o caminho do arquivo ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(folder):  # Lista todos os arquivos na pasta
            if file.endswith('.pdf'):  # Filtra apenas os arquivos PDF
                zipf.write(os.path.join(folder, file), arcname=file)  # Adiciona ao ZIP

    print(f'Arquivos compactados em {zip_path}')


# Função principal que realiza o Web Scraping para encontrar e baixar os PDFs desejados
def scrape_pdfs():
    response = requests.get(url)  # Faz a requisição para obter o conteúdo da página
    print(f"Status Code: {response.status_code}")  # Exibe o código de status da requisição

    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code != 200:
        print("Erro ao acessar a página!")
        return

    # Processa o conteúdo da página com BeautifulSoup para encontrar os links dos PDFs
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extrai todos os links que terminam com ".pdf" e remove duplicatas
    pdf_links = list(set(a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')))

    # Filtra apenas os PDFs cujo nome contém "Anexo_I" ou "Anexo_II"
    pdf_links_filtrados = [link for link in pdf_links if "Anexo_I" in link or "Anexo_II" in link]
    print(f'Encontrados {len(pdf_links_filtrados)} PDFs dos Anexos I e II.')

    # Se nenhum PDF dos anexos for encontrado, encerra a função
    if not pdf_links_filtrados:
        print("Nenhum PDF dos anexos encontrados!")
        return

    # Faz o download de cada PDF encontrado
    for link in pdf_links_filtrados:
        # Corrige links relativos, se necessário
        if not link.startswith('http'):
            link = 'https://www.gov.br' + link
        download_pdf(link, folder)

    # Após baixar todos os PDFs, compacta os arquivos em um ZIP
    compactar_pdfs(folder, 'anexos.zip')
