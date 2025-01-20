from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import SystemMessage, HumanMessage
import json
import os

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.2, max_tokens=3000)

SEPARATOR = "### NOVA_FATURA ###"
prompt_template = PromptTemplate(
    input_variables=["fields", "faturas"],
    template="""
    Você é um assistente especializado em análise de faturas de energia elétrica.
    Sua tarefa é extrair informações de múltiplas faturas com base nos campos fornecidos.
    Cada fatura será separada pelo delimitador "{separator}".

    ### Campos a serem extraídos:
    {fields}

    ### Faturas:
    {faturas}

    Com base nas faturas fornecidas, extraia as informações e devolva um JSON estruturado para cada fatura, separados por "{separator}".
    """
)

def load_extraction_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_invoice_texts(invoice_folder):
    invoices = []
    for filename in sorted(os.listdir(invoice_folder)):
        if filename.endswith(".txt"):
            with open(os.path.join(invoice_folder, filename), "r", encoding="utf-8") as f:
                invoices.append(f"Arquivo: {filename}\n{f.read().strip()}")
    return invoices

def process_invoices(config_path, invoice_folder):
    extraction_config = load_extraction_config(config_path)
    invoices = load_invoice_texts(invoice_folder)
    
    formatted_prompt = prompt_template.format(
        fields=json.dumps(extraction_config["fields_to_extract"], indent=4),
        faturas=f"\n{SEPARATOR}\n".join(invoices),
        separator=SEPARATOR
    )

    chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=[], template=formatted_prompt))
    response = chain.run({})

    json_blocks = response.split(SEPARATOR)
    
    output_folder = "data/raw/processed/"
    os.makedirs(output_folder, exist_ok=True)

    for i, json_text in enumerate(json_blocks):
        json_text = json_text.strip()
        if json_text:
            try:
                parsed_json = json.loads(json_text) 
                file_name = f"{output_folder}/invoice_{i+1}.json"
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(parsed_json, f, indent=4)
                print(f"✔ JSON salvo: {file_name}")
            except json.JSONDecodeError:
                print(f"⚠ Erro ao processar JSON da fatura {i+1}: {json_text}")

if __name__ == "__main__":
    config_path = "JSON_extract/Config_1.json"
    invoice_folder = "data/raw/preprocessed_text"

    if not os.path.exists(config_path):
        print(f"Erro: Configuração de extração não encontrada em {config_path}")
    elif not os.path.exists(invoice_folder):
        print(f"Erro: Pasta de faturas não encontrada em {invoice_folder}")
    else:
        process_invoices(config_path, invoice_folder)
