import mysql.connector
from datetime import datetime
import os
import validators  # Biblioteca para validar URLs
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': 'scraping_data'
}


def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None  # Retorna None se a conexão falhar


def insert_into_db(filename, url):
    conn = connect_db()
    if not conn:
        return  # Se a conexão falhar, sai da função

    if not validators.url(url):  # Valida a URL antes de inserir
        print(f"URL inválida: {url}")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO arquivos_pdf (nome_arquivo, url, data_download)
        VALUES (%s, %s, %s)
        """
        values = (filename, url, datetime.now())

        cursor.execute(query, values)
        conn.commit()
        print(f'{filename} salvo no banco de dados!')
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no banco: {err}")
    finally:
        cursor.close()
        conn.close()
