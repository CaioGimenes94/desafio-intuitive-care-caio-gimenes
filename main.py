from scraping.scrape import scrape_pdfs         # Importa a função responsável por baixar e compactar os PDFs
from database.transform import transform_data   # Importa a função que extrai e transforma os dados do PDF

# Ponto de entrada da aplicação
if __name__ == "__main__":
    scrape_pdfs()       # Executa o processo de scraping (baixa os PDFs e gera o ZIP)
    transform_data()    # Executa a transformação: extrai as tabelas do PDF, salva em CSV e compacta
