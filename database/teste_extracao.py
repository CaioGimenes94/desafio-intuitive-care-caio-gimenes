def save_tables_to_csv(tables, csv_path):
    """ Salva todas as tabelas extraídas em um único arquivo CSV """
    all_data = []

    for table in tables:
        df = pd.DataFrame(table)
        all_data.append(df)  # Adiciona cada tabela extraída

    if not all_data:
        print("Nenhuma tabela válida foi extraída.")
        return

    # Concatena todas as tabelas em um único DataFrame
    full_df = pd.concat(all_data, ignore_index=True)

    # Remove colunas totalmente vazias
    full_df = full_df.dropna(axis=1, how="all")

    # Define a primeira linha como cabeçalho correto e remove a duplicação
    full_df.columns = full_df.iloc[0].astype(str).apply(lambda x: normalize_text(clean_text(x))).str.strip()
    full_df = full_df[1:].reset_index(drop=True)  # Remove a linha duplicada e reseta os índices

    # Remove linhas que são idênticas ao cabeçalho
    full_df = full_df[full_df.apply(lambda row: not all(row == full_df.columns), axis=1)].reset_index(drop=True)

    # Aplica a correção de caracteres corrompidos nos dados
    full_df = full_df.applymap(lambda x: normalize_text(clean_text(x)))

    # Substitui valores das colunas OD e AMB
    for coluna, mapa in SUBSTITUICOES.items():
        if coluna in full_df.columns:
            full_df[coluna] = full_df[coluna].astype(str).str.strip()  # Remove espaços extras
            full_df[coluna] = full_df[coluna].map(mapa).fillna(full_df[coluna])  # Aplica substituição

    # Salva o DataFrame no CSV com separador correto
    full_df.to_csv(csv_path, index=False, encoding="utf-8", sep=";")  # Usa ";" como separador

    print(f"Tabelas extraídas e transformadas salvas em {csv_path}")


    #
    #
    #
    #

import os
import pandas as pd
import pdfplumber
import zipfile
import ftfy                  # Corrige caracteres corrompidos em textos
import unicodedata           # Utilizado para normalizar acentuação de caracteres

# Define os caminhos principais dos arquivos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Caminho base do projeto
PDF_PATH = os.path.join(BASE_DIR, "data", "pdfs", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")  # Caminho do PDF de entrada
CSV_PATH = os.path.join(BASE_DIR, "data", "extracted_data.csv")                                   # Caminho do CSV de saída
ZIP_PATH = os.path.join(BASE_DIR, "data", "Teste_Caio_Gimenes.zip")                               # Caminho do ZIP final

# Mapeia siglas dos campos OD e AMB para textos mais legíveis
SUBSTITUICOES = {
    "OD": {"S": "Seg. Odontológica", "N": "Não"},
    "AMB": {"S": "Seg. Ambulatorial", "N": "Não"}
}

def extract_tables_from_pdf(pdf_path):
    """ Extrai todas as tabelas presentes em todas as páginas do PDF """
    extracted_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()  # Extrai todas as tabelas da página atual
            extracted_tables.extend(tables)  # Adiciona à lista final
    return extracted_tables

def clean_text(text):
    """ Corrige caracteres corrompidos usando a biblioteca ftfy """
    if isinstance(text, str):
        return ftfy.fix_text(text).strip()  # Remove espaços e caracteres quebrados
    return text

def normalize_text(text):
    """ Remove acentuação dos caracteres, facilitando comparações """
    if isinstance(text, str):
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")
    return text

def save_tables_to_csv(tables, csv_path):
    """ Limpa e salva todas as tabelas extraídas do PDF em um único arquivo CSV """
    all_data = []

    # Converte cada tabela bruta em DataFrame e armazena
    for table in tables:
        df = pd.DataFrame(table)
        all_data.append(df)

    # Se não houver nenhuma tabela válida, encerra a função
    if not all_data:
        print("Nenhuma tabela válida foi extraída.")
        return

    # Junta todas as tabelas em um único DataFrame
    full_df = pd.concat(all_data, ignore_index=True)

    # Remove colunas que estão completamente vazias
    full_df = full_df.dropna(axis=1, how="all")

    # Ajusta os nomes das colunas: utiliza a primeira linha como cabeçalho
    full_df.columns = full_df.iloc[0].astype(str).apply(lambda x: normalize_text(clean_text(x))).str.strip()
    full_df = full_df[1:].reset_index(drop=True)  # Remove a linha duplicada do cabeçalho

    # Remove linhas que sejam idênticas ao cabeçalho (ocorre em alguns PDFs)
    full_df = full_df[full_df.apply(lambda row: not all(row == full_df.columns), axis=1)].reset_index(drop=True)

    # Aplica limpeza de texto e normalização em todas as células
    full_df = full_df.applymap(lambda x: normalize_text(clean_text(x)))

    # Substitui valores das colunas com "OD" e "AMB", se encontradas, com base no dicionário SUBSTITUICOES
    for coluna, mapa in SUBSTITUICOES.items():
        for col_name in full_df.columns:
            if coluna in normalize_text(col_name).upper():  # Ex: "OD" ou "AMB"
                full_df[col_name] = full_df[col_name].astype(str).str.strip()
                full_df[col_name] = full_df[col_name].map(mapa).fillna(full_df[col_name])  # Substitui os valores mapeados

    # Salva o DataFrame como CSV com separador ";"
    full_df.to_csv(csv_path, index=False, encoding="utf-8", sep=";")

    print(f"Tabelas extraídas e transformadas salvas em {csv_path}")

def compress_csv(zip_path, csv_path):
    """ Compacta o arquivo CSV em um arquivo ZIP """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))  # Usa apenas o nome do arquivo dentro do ZIP

def transform_data():
    """ Executa todo o processo: extrair, tratar, salvar e compactar os dados """
    print("Extraindo tabelas do PDF...")
    tables = extract_tables_from_pdf(PDF_PATH)

    # Se nenhuma tabela foi extraída, exibe mensagem e encerra
    if not tables:
        print("Nenhuma tabela encontrada.")
        return

    print("Salvando os dados em CSV...")
    save_tables_to_csv(tables, CSV_PATH)

    print("Compactando o arquivo CSV...")
    compress_csv(ZIP_PATH, CSV_PATH)

    print("Processo concluído!")

# Ponto de entrada da execução quando o script é rodado diretamente
if __name__ == "__main__":
    transform_data()
