import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

DB_CONFIG = {
    'host': 'localhost',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': 'scraping_data'
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def insert_into_db(filename, url):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO arquivos_pdf (nome_arquivo, url, data_download)
    VALUES (%s, %s, %s)
    """
    values = (filename, url, datetime.now())

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
    print(f'{filename} salvo no banco de dados!')
