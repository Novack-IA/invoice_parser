# 📄 INVOICE PARSER - Processador Inteligente de Faturas

## 📌 Descrição do Projeto
O **Invoice Parser** é um sistema automatizado para **extração e processamento de faturas em PDF** utilizando **Visão Computacional, Processamento de Linguagem Natural (NLP) e Large Language Models (LLMs)**. Ele permite que usuários **arrastem e soltem faturas na interface**, extraindo informações importantes e gerando **arquivos JSON estruturados**.

## 🚀 Funcionalidades
- 🔹 **Interface Drag-and-Drop** para fácil carregamento de faturas.
- 🔹 **Extração automática de texto de PDFs** usando `pdfplumber` e OCR (`pytesseract`).
- 🔹 **Geração dinâmica de prompts** para envio ao `GPT-4o` via `LangChain`.
- 🔹 **Armazenamento estruturado** dos JSONs processados.
- 🔹 **Execução escalável**, suportando múltiplas faturas no mesmo prompt.

## 📂 Estrutura do Projeto
```
INVOICE_PARSER/
├── data/
│   ├── raw/
│   │   ├── invoices/          # PDFs enviados para processamento
│   │   ├── extracted_text/    # Texto extraído das faturas
│   │   ├── preprocessed_text/ # Texto preprocessado  
│   │   ├── processed/         # JSONs gerados após processamento
│
├── scripts/
│   ├── extract_text.py        # Extrai texto dos PDFs
│   ├── preprocess_text.py     # Preprocessa o texto extraído
│   ├── validate_JSON.py       # Valida o JSON gerado pela LLM verificando os campos requisitados pela configuração
│   ├── llm_api_requester.py   # Gera prompts e envia ao GPT-4o, obtendo o JSON estruturado 
│
├── interface/
│   ├── gui.py                 # Interface gráfica drag-and-drop
│
├── JSON_Extract/              # Configurações JSON para extração dinâmica
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências do projeto
└── .gitignore                 # Arquivos a serem ignorados no repositório
```

## 🛠️ Tecnologias Utilizadas
- **Python 3.9+**
- **Tkinter + tkinterdnd2** (Interface gráfica Drag-and-Drop)
- **LangChain** (Orquestração de prompts para GPT-4o)
- **OpenAI API** (Integração com LLMs)
- **pdfplumber** e **pytesseract** (Extração de texto de PDFs)

## 🏗️ Como Configurar e Executar

### **1️⃣ Clonar o repositório**
```bash
git clone https://github.com/seu-usuario/invoice_parser.git
cd invoice_parser
```

### **2️⃣ Criar e ativar o ambiente virtual**
```bash
python -m venv venv  # Criar ambiente virtual
```
✅ **Ativar o ambiente virtual:**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### **3️⃣ Instalar as dependências**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure sua chave da OpenAI**
Defina sua chave da OpenAI no ambiente:
```bash
export OPENAI_API_KEY="sua-chave-aqui"  # Linux/macOS
set OPENAI_API_KEY="sua-chave-aqui"  # Windows
```
Ou configure diretamente no `settings.json` do VS Code.

### **5️⃣ Execute a Interface**
```bash
python interface/gui.py
```
Isso abrirá a interface para **arrastar e soltar PDFs**.

### **6️⃣ Verifique os JSONs Gerados**
Após o processamento, os JSONs estarão disponíveis em:
```bash
data/raw/processed/
```

## 🛠️ Como Funciona o Pipeline
1️⃣ O **usuário arrasta um arquivo PDF** para a interface.
2️⃣ O arquivo é **movido para `data/raw/invoices/`**.
3️⃣ `extract_text.py` **extrai o texto** do PDF.
4️⃣ `llm_api_requester.py` **gera o prompt e envia para GPT-4o**.
5️⃣ O GPT-4o retorna os **dados extraídos em JSON**.
6️⃣ O JSON é salvo em `data/raw/processed/` e pode ser acessado via a interface.

## 📌 Contribuindo
Quer contribuir? Sinta-se à vontade para abrir issues e pull requests. 😉

## 📝 Licença
Este projeto é distribuído sob a **MIT License**.

