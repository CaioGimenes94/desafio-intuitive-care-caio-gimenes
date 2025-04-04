# Desafio Técnico

Este projeto automatiza o processo de scraping, transformação e compactação de dados publicados pela ANS (Agência Nacional de Saúde Suplementar), especificamente os arquivos dos Anexos I e II do Rol de Procedimentos.

---

## 🛠️ Funcionalidades

1. **Web Scraping:**  
   - Acessa o site oficial da ANS.  
   - Localiza e baixa os PDFs dos **Anexos I e II**.  
   - Salva os arquivos localmente e registra seus nomes, URLs e data de download no banco de dados MySQL.
   - Compactação de todos os anexos em um único arquivo.  


2. **Transformação de Dados (Anexo I):**  
   - Extrai todas as tabelas do PDF.  
   - Limpa e normaliza os dados (acentuação, caracteres quebrados, etc).  
   - Converte para CSV (`extracted_data.csv`).  
   - Compacta o CSV em um `.zip` chamado `Teste_Caio_Gimenes.zip`.

---

## 🧰 Tecnologias Utilizadas

- Python 3
- `requests`, `beautifulsoup4`, `pdfplumber`, `pandas`
- `mysql-connector-python`, `python-dotenv`, `validators`, `ftfy`
- Banco de dados MySQL
- Estrutura modular com pastas: `scraping`, `database`, `data`

---

## Estrutura do Projeto
```
📦 desafio-intuitive-care
├── 📂 data
│   ├── 📂 pdfs
│       ├── PDFs baixados
│       ├── anexos.zip
│   ├── extracted_data.csv  
│   ├── Teste_Caio_Gimenes.zip
├── 📂 scraping
│   ├── scrape.py
├── 📂 transform
│   ├── transform.py
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Executar

1. Clone o repositório:
   ```
   git clone <URL>
   cd <nome-do-projeto>

2. Instale as dependências:
   ```
   pip install -r requirements.txt

3. Configure o arquivo .env:
   ```
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   
4. Certifique-se de ter o banco de dados MySQL rodando com a seguinte tabela:
   ```
   CREATE DATABASE scraping_data;

   CREATE TABLE arquivos_pdf (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nome_arquivo VARCHAR(255),
       url TEXT,
       data_download DATETIME
   );

5. Execute o script principal:
   ```
   python main.py
   
---

## 📌 Observações
- A execução pode levar alguns segundos, especialmente na extração de dados do PDF.


- O script foi testado com o PDF do Anexo I referente à RN 465/2021 e RN 627/2024.

---

## 📝 Nota de Transparência
Não consegui finalizar as partes 3 e 4 por limitações técnicas, mas me comprometi a entregar um projeto funcional.

Também utilizei o ChatGPT para estruturar, organizar meu tempo e desenvolver o código. Acredito que isso demonstra minha proatividade em resolver problemas e aprender. Se tiver a chance de seguir no processo, continuarei me aperfeiçoando.
No dia a dia, aprender com a equipe faz toda a diferença, e não vejo a hora de ter essa oportunidade.

---

## 👨‍💻 Autor
Caio Gimenes | Desafio técnico - Intuitive Care